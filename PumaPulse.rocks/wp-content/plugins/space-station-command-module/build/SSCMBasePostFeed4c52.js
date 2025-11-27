window.SpaceStation = window.SpaceStation || {};
window.SpaceStation.CommandModule = window.SpaceStation.CommandModule || {};
window.SpaceStation.CommandModule.PostFeed = window.SpaceStation.CommandModule.PostFeed || {};

(function(module, Behaviors, $) {
    /**
     * Behavior for a post feed set to 'grid' or 'list' mode.
     * 
     * TODO: This Behavior has a very significant jQuery dependency.
     * It should be refactored to bare DOM.
     */
    class PostFeed extends Behaviors.Behavior {
        static QUERY = "[data-sscmbasepostfeed]";

        /**
         * The AJAX hook to use to fetch pages of the post feed.
         */
        static RENDER_PAGE_ACTION = "sscmbasepostfeed_renderpage";

        constructor(...args) {
            super(...args);

            this.request_uri = this.elem.dataset.sscmbasepostfeedRequesturi;
            this.query_vars = this.elem.dataset.sscmbasepostfeedQueryvars;
            this.layout_id = this.elem.dataset.sscmbasepostfeedLayoutid;
            this.wrapper_id = this.elem.dataset.sscmbasepostfeedWrapperid;
            this.pagination_mode = this.elem.dataset.sscmbasepostfeedPaginationmode;

            //Selectors for elements we plan to attach stuff to.
            //These COULD be static properties, but we need to customize them
            //with our node ID.
            this.found_post_identifier = `#SSCMBasePostFeed-found_posts-${this.wrapper_id}`;
            this.post_feed_selector = `#SSCMBasePostFeed-taxonomy_selectors-${this.wrapper_id}` + ' select';
            this.post_feed_tab_selector = `#SSCMBasePostFeed-taxonomy_selectors-${this.wrapper_id}` + ' .SSCMBasePostFeed-tab_taxonomies';
            this.post_feed_checkbox_selector = `#SSCMBasePostFeed-taxonomy_selectors-${this.wrapper_id}` + ' .SSCMBasePostFeed-checkbox_taxonomies';
            this.search_container = `#SSCMBasePostFeed-search_container-${this.wrapper_id}`;
            this.results_selector = `#results-${this.wrapper_id}`;
            this.prev = `.prev-button-${this.wrapper_id}`;
            this.next = `.next-button-${this.wrapper_id}`;
            this.loadMoreButton = `#SSCMBasePostFeed-load_more_btn-${this.wrapper_id}`;

            // UI state
            this.current_page = parseInt($(this.found_post_identifier).data("current-page"));
            this.locked = false;

            this.apply_settings_from_url();
            this.initialize_feed();
            $(this.loadMoreButton).click(this.loadMorePosts.bind(this));
            $(this.post_feed_selector).on('change', this.select_change_intent.bind(this));

         

            let all_tabs = document.querySelectorAll(this.post_feed_tab_selector + ' .SSCMBasePostFeed-tab_taxonomy');

            for( let i = 0; i< all_tabs.length; i++){
                all_tabs[i].addEventListener('click', this.tab_change_intent.bind( this ));
            }

            this.search_container_elem = document.querySelector(this.search_container);
            if (this.search_container_elem) {
                this.search_container_elem.addEventListener('change', this.search_change_intent.bind(this));
                this.search_container_elem.addEventListener('keyup', this.search_change_intent.bind(this));
            }

            $(document).on('change', this.post_feed_checkbox_selector + ' input[type="checkbox"]', this.checkbox_change_intent.bind(this));
            $(document).on('click', this.results_selector + ' .filter-tag .remove-tag', this.filter_remove_intent.bind(this));

            // For each checkbox
            $(this.post_feed_checkbox_selector + ' input[type="checkbox"]').each(function () {
                // If this checkbox is checked
                if ($(this).is(':checked')) {
                    // Get the label of this checkbox
                    var label = $(this).next('label').text();

                    // Add a tag for this checkbox
                    $(this.results_selector + ' .selected-filters').append('<span class="filter-tag" data-id="' + $(this).attr('id') + '">' + label + ' <span class="remove-tag">x</span></span>');
                }
            });
        }

        /**
         * Lock the filters to prevent clicking on anything while a load is
         * happening.
         */
        lock_filters() {
            this.locked = true;
            
            $(this.prev).prop("disabled", true);
            $(this.next).prop("disabled", true);
        }

        /**
         * Unlock filters to allow clicking on things once a load finishes.
         */
        unlock_filters() {
            this.locked = false;
            
            this.toggleNextPrevBtn();
        }

        max_page() {
            var maybe_max_page = parseInt($('.SSCMBasePostFeed-post-' + this.wrapper_id).attr('data-post-max-page'));

            if (isNaN(maybe_max_page)) {
                maybe_max_page = 1;
            }

            return maybe_max_page;
        }
        
        /**
         * Load a given page into the feed from the backend.
         * 
         * This is intended to connect to the AJAX hook in loader.decl.php,
         * which will load and render the given post/node ID with our filter
         * settings (sanitized, of course, but that's PHP's concern, not ours)
         * 
         * This also handles updating the URL, current page number, and
         * pagination.
         * 
         * @param {Number} page The page number to load.
         * @param {Boolean} isLoadMore TRUE if this is the result of clicking
         * a Load More button. Load More buttons keep old posts in the feed.
         */
        load_page(page, isLoadMore = false) {
            function load_page_inner() {
                let filters = this.getFilters();

                if (this.locked) {
                    if (this.load_page_timeout) {
                        window.clearTimeout(this.load_page_timeout);
                    }

                    this.load_page_timeout = window.setTimeout(() => load_page_inner.apply(this), 200);
                    return;
                }

                this.lock_filters();
                this.load_page_timeout = null;

                let maxPage = this.max_page();
                let clampedPage = Math.min(page, maxPage);

                $.ajax({
                    url: window.SpaceStation.CommandModule.SSCMBasePostFeed.admin_ajax_url,
                    method: 'get',
                    data: {
                        action: PostFeed.RENDER_PAGE_ACTION,
                        request_uri: this.request_uri,
                        query_vars: this.query_vars,
                        layout_id: this.layout_id,
                        node_id: this.wrapper_id,
                        _page: clampedPage,
                        filters,
                    },
                    success: function (response) {
                        let $listItems = $(response).find('.SSCMBasePostFeed-post'),
                            $listContainer = $('#SSCMBasePostFeed-posts_container-' + this.wrapper_id),
                            $emptyResult = $(response).find(".SSCMBasePostFeed-no_post_found");
        
                        // Remove existing list items from container
                        if (!isLoadMore) {
                            $listContainer.empty();
                        }
        
                        // Append new list items to existing container
                        $listContainer.append($listItems);

                        while ($listContainer.next().length > 0) {
                            $listContainer.next().remove();
                        }
                        $listContainer.after($emptyResult);

                        this.current_page = clampedPage;

                         
                        this.update_url(filters, clampedPage);
                        
        
                        // Update pagination and other necessary elements
                        this.unlock_filters();
                        this.buildPagination();
        
                        // Trigger content ready event
                        Behaviors.content_ready($listContainer.get(0));
                    }.bind(this)
                });
            }

            if (this.load_page_timeout) {
                window.clearTimeout(this.load_page_timeout);
            }

            this.load_page_timeout = window.setTimeout(() => load_page_inner.apply(this), 200);
        }

        /**
         * Update the URL displayed to the user with the page and filter
         * settings.
         * 
         * This should be called with the settings used in the last page
         * request, so that the currently displayed content and URL are always
         * synchronized.
         * 
         * @param {Object} settings The settings object, usually obtained from
         * getFilters.
         * 
         * @param {Number} page The requested page.
         */
        update_url(settings, page) {
            let currentURL = window.location.href;
            let params = new URLSearchParams(currentURL.split('?')[1]);

            params.set('_page', page);

            for (let taxonomy in settings.checkboxes) {
                if (settings.checkboxes.hasOwnProperty(taxonomy)) {
                    let key = `${taxonomy.replace('-select', '')}[]`,
                        terms = settings.checkboxes[taxonomy];
                    
                    params.delete(key);
                    
                    if (terms.length > 0) {
                        terms.forEach(term => {
                            params.append(key, term);
                        });
                    }
                }
            }

            for (let taxonomy in settings.selects) {
                if (settings.selects.hasOwnProperty(taxonomy)) {
                    let term = settings.selects[taxonomy];
                    if (term) {
                        params.set(taxonomy, term);
                    }
                }
            }

            params.delete("keyword");
            if (settings.keyword) {
                params.set("keyword", settings.keyword);
            }

            if (history.pushState) {

                // don't display _page=1 on page load
                if ( ! window.location.search.includes('_page')) {
                    params.delete('_page','1');
                }
                
                history.pushState(null, null, (  params.size >= 1 ? '?' : '') + params.toString());                

            }
        }

        /**
         * Apply URL parameters to the checkboxes, dropdowns, tabs, and text fields
         * on the current post feed.
         * 
         * TODO: Resolve what happens when there are multiple post feeds on
         * the same page.
         */
        apply_settings_from_url() {
            let searchParams = new URLSearchParams(window.location.search);
            
            $(this.post_feed_checkbox_selector + ' input[type="checkbox"]').each(function () {
                let checkbox = $(this);
                let taxonomy = checkbox.attr("name");
                if (searchParams.has(taxonomy)) {
                    let terms = searchParams.get(taxonomy).split(",");
                    checkbox.prop("checked", terms.includes(checkbox.val()));
                }
            });

            $(this.post_feed_selector).each(function () {
                let $select = $(this);
                let taxonomy = $select.attr("name");
                let post_type = $select.data('post-type');
                let property = 'tax_' + post_type + '_' + taxonomy;

                if (searchParams.has(property)) {
                    $select.val(searchParams.get(property));
                }
            });


            $(this.post_feed_tab_selector).each(function () {
                let $select = $(this);
                let taxonomy = $select.attr("data-tax-name");
                let post_type = $select.data('post-type');
                let property = 'tax_' + post_type + '_' + taxonomy;

                if (searchParams.has(property)) {
                    $select.attr('data-filter-value', searchParams.get(property));

                    $(`.SSCMBasePostFeed-tab_taxonomy[data-tax-name="${taxonomy}"][data-filter-value="${searchParams.get(property)}"]`).addClass('selected'); //select
                }
            });

            if (searchParams.has("keyword")) {
                $(this.search_container + ' .SSCMBasePostFeed-search_field').val(searchParams.get("keyword"));
            } else {
                $(this.search_container + ' .SSCMBasePostFeed-search_field').val("");
            }
            
            if (searchParams.has("_page")) {
                this.current_page = parseInt(searchParams.get("_page"));
                if (isNaN(this.current_page)) {
                    this.current_page = 1;
                }
            } else {
                this.current_page = 1;
            }
        }
        
        /**
         * Update the state of the next and previous buttons, based on the
         * current and total page counts.
         */
        toggleNextPrevBtn() {
            let maxPage = this.max_page();

            $(this.prev).prop("disabled", this.current_page === 1);
            $(this.next).prop("disabled", this.current_page === maxPage || maxPage === 0);
            $(this.prev).prop("disabled", maxPage <= 1 || this.current_page <= 1);
            $(this.next).prop("disabled", maxPage <= 1 || this.current_page >= maxPage);
        }

        /**
         * Attach event handlers for the pagination being clicked.
         * 
         * This should be called every time the pagination is rebuilt.
         */
        bindPaginationEventClick() {
            var that = this;

            this.toggleNextPrevBtn();
            $(`.SSCMBasePostFeed-page_link-${this.wrapper_id}`).on('click', function (e) {
                that.pagination_click_intent(e, this);
            });

            $(this.prev).on("click", function(e) {
                if (this.current_page > 1) {
                    this.load_page(this.current_page - 1, false);
                    this.toggleNextPrevBtn();
                }
            }.bind(this));

            $(this.next).on("click", function(e) {
                let maxPage = this.max_page();
                if (this.current_page <= maxPage) {
                    this.load_page(this.current_page + 1, false);
                    this.toggleNextPrevBtn();
                }
            }.bind(this));
        }

        /** 
         * Event handler for page buttons being clicked.
         */
        pagination_click_intent(e, clicked_elem) {
            if (this.locked) return;

            // Get the clicked page number
            let new_page = parseInt($(clicked_elem).data('page'));

            this.current_page = new_page;
            this.load_page(new_page, false);

            this.toggleNextPrevBtn();
        }

        /**
         * Hide or show the pagination depending on if there are multiple
         * pages or not.
         */
        togglePaginationVisibility() {
            let maxPage = this.max_page();
            if (isNaN(maxPage) || maxPage <= 1) {
                $(`#SSCMBasePostFeed-pagination_container-${this.wrapper_id}`).hide();
            } else {
                $(`#SSCMBasePostFeed-pagination_container-${this.wrapper_id}`).show();
            }
        }

        /**
         * Update (or create for the first time) user-facing pagination controls.
         */
        buildPagination() {
            let maxPage = this.max_page();

            if (this.pagination_mode === "pages") {


                // Remove existing pagination items
                $(`#SSCMBasePostFeed-pagination-${this.wrapper_id} .SSCMBasePostFeed-page_item`).remove();

                // Always add first page
                $(`#SSCMBasePostFeed-pagination-${this.wrapper_id}`).append(`
                    <li id="SSCMBasePostFeed-page_item-${this.wrapper_id}" class="SSCMBasePostFeed-page_item">
                        <a href="javascript:;" class="SSCMBasePostFeed-page_link SSCMBasePostFeed-page_link-${this.wrapper_id}" data-page="1">1</a>
                    </li>
                `);

                // Add ellipsis if current page is more than 3 pages away from start
                if (this.current_page > 3) {
                    $(`#SSCMBasePostFeed-pagination-${this.wrapper_id}`).append(`
                        <li class="SSCMBasePostFeed-page_item SSCMBasePostFeed-ellipsis">
                            <span>...</span>
                        </li>
                    `);
                }

                // Calculate start and end pages to show around current page
                const startPage = Math.max(2, this.current_page - 1);
                const endPage = Math.min(maxPage - 1, this.current_page + 1);



                // Add pages around current page
                for (let i = startPage; i <= endPage; i++) {
                    $(`#SSCMBasePostFeed-pagination-${this.wrapper_id}`).append(`
                        <li id="SSCMBasePostFeed-page_item-${this.wrapper_id}" class="SSCMBasePostFeed-page_item">
                            <a href="javascript:;" class="SSCMBasePostFeed-page_link SSCMBasePostFeed-page_link-${this.wrapper_id}" data-page="${i}">${i}</a>
                        </li>
                    `);
                }

                // Add ellipsis if current page is more than 3 pages away from end
                if (this.current_page < maxPage - 2) {
                    $(`#SSCMBasePostFeed-pagination-${this.wrapper_id}`).append(`
                        <li class="SSCMBasePostFeed-page_item SSCMBasePostFeed-ellipsis">
                            <span>...</span>
                        </li>
                    `);
                }

                // Add last page if there's more than 1 page
                if (maxPage > 1) {
                    $(`#SSCMBasePostFeed-pagination-${this.wrapper_id}`).append(`
                        <li id="SSCMBasePostFeed-page_item-${this.wrapper_id}" class="SSCMBasePostFeed-page_item">
                            <a href="javascript:;" class="SSCMBasePostFeed-page_link SSCMBasePostFeed-page_link-${this.wrapper_id}" data-page="${maxPage}">${maxPage}</a>
                        </li>
                    `);
                }


                $('.SSCMBasePostFeed-page_link[data-page="' + this.current_page + '"]').parent().addClass('active');

                this.bindPaginationEventClick();
                this.togglePaginationVisibility();
            } else if (this.pagination_mode === "load_more") {
                // Remove all existing "Load More" buttons
                $(`#SSCMBasePostFeed-load_more_btn-${this.wrapper_id}`).remove();

                // Check if the current page is less than the maximum page
                if (this.current_page < maxPage) {
                    // Add the "Load More" button
                    $(`#SSCMBasePostFeed-pagination_container-${this.wrapper_id}`).append(`
                        <button id="SSCMBasePostFeed-load_more_btn-${this.wrapper_id}" class="SSCMBasePostFeed-load_more_btn">
                            Load More
                        </button>
                    `);
                    
                    // Attach the click event to the "Load More" button
                    $(this.loadMoreButton).click(this.loadMorePosts.bind(this));
                }
            }
        }

        /**
         * Extract filter settings from the current UI state and package it into
         * an object to be sent to the server.
         * 
         * @returns An object with the following keys:
         * 
         *  - checkboxes: The state of each taxonomy checkbox
         *  - selects: The selected option for each taxonomy select
         *  - keyword: The search keyword (if entered)
         */
        getFilters() {
            let settings = {
                checkboxes: {},
                selects: {},
                tabs: {}
            };
    
            // Collect the checked checkboxes to the filters
            $(this.post_feed_checkbox_selector).each(function () {
                let taxonomy = $(this).attr('id');
                settings.checkboxes[taxonomy] = settings.checkboxes[taxonomy] || []; // Initialize the array if it doesn't exist
                $(this).find('input:checked').each(function () {
                    settings.checkboxes[taxonomy].push($(this).val());
                });
            });
    
            // And the same but for the selects
            $(this.post_feed_selector).each(function () {
                let selectedValue = $.trim($(this).val());
                if (selectedValue.startsWith('all-')) { //All options clear specific filters off
                    let taxonomy = selectedValue.split("all-")[1];
                    let property = 'tax_' + $(this).data('post-type') + '_' + taxonomy;
                    settings.selects[property] = '';
                } else if (selectedValue) {
                    let property = 'tax_' + $(this).data('post-type') + '_' + $(this).attr("name");
                    settings.selects[property] = selectedValue;
                }
            });

            // tabs
            $(this.post_feed_tab_selector).each(function () {
                let selectedValue = $.trim($(this).attr('data-filter-value'));
                if (selectedValue.startsWith('all-')) { //All options clear specific filters off
                    let taxonomy = selectedValue.split("all-")[1];
                    let property = 'tax_' + $(this).data('post-type') + '_' + taxonomy;
                    settings.tabs[property] = '';
                } else if (selectedValue) {
                    let property = 'tax_' + $(this).data('post-type') + '_' + $(this).attr("data-tax-name");
                    settings.tabs[property] = selectedValue;
                }

            });
    
            // Now the text search, if present
            $(this.search_container + ' .SSCMBasePostFeed-search_field').each(function() {
                settings.keyword = $(this).val();
            });
    
            return settings;
        }

        /**
         * Render the first page of whatever the current selected filters are.
         * 
         * This triggers the first page load, populates the filter tags, and
         * builds the pagination. It should not be called outside of
         * initialization.
         */
        initialize_feed() {
            this.buildPagination();
            this.load_page(this.current_page, false);

            // Get the checkbox label
            let label = $("label[for='" + $(this).attr('id') + "']").text();

            // Check if the checkbox is checked or unchecked
            if ($(this).is(':checked')) {
                // The checkbox is checked, add a tag
                $(this.results_selector + ' .selected-filters').append('<span class="filter-tag" data-id="' + $(this).attr('id') + '">' + label + ' <span class="remove-tag">x</span></span>');
            } else {
                // The checkbox is unchecked, remove the tag
                $(this.results_selector + ' .selected-filters .filter-tag[data-id="' + $(this).attr('id') + '"]').remove();
            }
        }

        /**
         * Event handler for the Load More button.
         */
        loadMorePosts() {
            this.load_page(this.current_page + 1, true);
        }

        /**
         * Event handler for the select dropdowns used to select filter
         * categories on the post feed.
         */
        select_change_intent() {
            this.load_page(1, false);
    
            //TODO: This should be replaced with / integrated into update_url
            let data_arr = [];
            $(`${this.post_feed_selector}`).each(function () {
                if ($.trim($(this).val())) {
                    data_arr.push($(this).attr("name") + '=' + $(this).val());
                }
            });

            let joined_data = data_arr.join('&');
            let loc = jQuery('<a>', {href: window.location})[0];
            if (history.pushState) {
                history.pushState(null, null, loc.pathname + '?' + joined_data);
            }
            this.current_page = 1;
        }

        /**
         * Event handler for the tab/button selection to select filter
         * categories on the post feed.
         */
        tab_change_intent(e) {

            e.target.parentNode.setAttribute('data-filter-value', e.target.getAttribute('data-filter-value'));


            //remove selected class to other tabs
            let all_tabs = document.querySelectorAll(this.post_feed_tab_selector + ' .SSCMBasePostFeed-tab_taxonomy');

            for( let i = 0; i< all_tabs.length; i++){
                if( all_tabs[i].isEqualNode(e.target )) { //test DOM equality
                    e.target.classList.add('selected');
                }else{
                    all_tabs[i].classList.remove('selected');
                }
            }

            
            let data_arr = [];

            let tax_name = e.target.getAttribute('data-tax-name');
            let tax_value = e.target.getAttribute('data-filter-value');
            let post_type = e.target.getAttribute('data-post-type');

            data_arr.push( tax_name + '%5B%5D=' +  tax_value);

            data_arr.push( 'tax_' + post_type + '_' + tax_name + '=' +  tax_value);

            let joined_data = data_arr.join('&');
            let loc = jQuery('<a>', {href: window.location})[0];
            if (history.pushState) {
                history.pushState(null, null, loc.pathname + '?' + joined_data);
            }

            this.current_page = 1;
            this.load_page(1, false); // false here to get a fresh set of posts not appending to existing ones
            
        }

        /**
         * Event handler for the search field on the post feed.
         * 
         * This event handler is debounced: event will only trigger after 500ms of no input.
         */
        search_change_intent() {
            this.load_page(1, false);
            this.current_page = 1;
        }

        /**
         * Event handler for the checkboxes used to select filter categories
         * on the post feed.
         */
        checkbox_change_intent() {
            this.current_page = 1;
            this.load_page(1, false); // false here to get a fresh set of posts not appending to existing ones

            // Get the checkbox label
            let label = $("label[for='" + $(this).attr('id') + "']").text();

            // Update list of enabled options displayed to the user.
            // First, clear the list, then add all the currently-checked tags.
            $(this.results_selector + ' .selected-filters .filter-tag[data-id="' + $(this).attr('id') + '"]').remove();
            if ($(this).is(':checked')) {
                $(this.results_selector + ' .selected-filters').append('<span class="filter-tag" data-id="' + $(this).attr('id') + '">' + label + ' <span class="remove-tag">x</span></span>');
            }
        }

        /**
         * Event handler for clicking the remove button on an active filter.
         */
        filter_remove_intent() {
            // Get the tag element
            let tagElement = $(this).parent('.filter-tag');
    
            // Get the id of the associated checkbox
            let checkboxId = tagElement.data('id');
    
            // Uncheck the checkbox
            $('#' + checkboxId).prop('checked', false);
    
            // Remove the tag
            tagElement.remove();
    
            // Update the filters
            this.current_page = 1;
            this.load_page(1, false); // false here to get a fresh set of posts not appending to existing ones
        }
    }

    Behaviors.register_behavior(PostFeed);

    module.PostFeed = PostFeed;

    return PostFeed;
}(window.SpaceStation.CommandModule.PostFeed, window.EVASuit.Behaviors, window.jQuery));
//# sourceMappingURL=SSCMBasePostFeed.js.map
