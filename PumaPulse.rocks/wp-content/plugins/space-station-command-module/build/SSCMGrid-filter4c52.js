window.SpaceStation = window.SpaceStation || {};
window.SpaceStation.CommandModule = window.SpaceStation.CommandModule || {};
window.SpaceStation.CommandModule.Grid = window.SpaceStation.CommandModule.Grid || {};

window.SpaceStation.CommandModule.Grid.Filter = (function(Behaviors) {
    class Filter extends Behaviors.Behavior {
        static QUERY = "[data-sscmgrid-filter]";
        static TABS_QUERY = "[data-sscmgrid-filtertab]";
        static SLIDER_QUERY = "[data-sscmgrid-titles]";
        static ITEMS_QUERY = "[data-sscmgrid-itemcategories]";
        static DROPDOWN_QUERY = ".SSCMGrid-filter_tabs-mobile_dropdown";

        constructor(...args) {
            super(...args);

            this.tabs = this.elem.querySelectorAll(Filter.TABS_QUERY);
            this.slider = this.elem.querySelectorAll(Filter.SLIDER_QUERY);
            this.items = this.elem.querySelectorAll(Filter.ITEMS_QUERY);

            this.tabs.forEach((t) => t.addEventListener("click", this.filter_intent.bind(this, t)));


            this.dropdown_options = this.elem.querySelectorAll( Filter.DROPDOWN_QUERY );

            let that = this.elem;

            this.dropdown_options.forEach( (t) => t.addEventListener("change", (e) => {
                let selectedValue = e.target.value;

                let domQuery = '[data-sscmgrid-filtertab="' + selectedValue + '"]';

                let targetTabElement = that.querySelector( domQuery );

                if( targetTabElement ){
                    targetTabElement.dispatchEvent(new Event('click'));
                    
                }else{
                    //trigger all
                    let all = that.querySelector('[data-sscmgrid-filtertab-all]' );

                    if( all ){
                        all.dispatchEvent( new Event('click'));
                    }
                }

            }));


            window.addEventListener('resize', () => {
                //account for resize, mobile filter should also be updated

                let selectedFilter = that.querySelector('.is-SSCMGrid-filter_tab--active');

                if( selectedFilter ){
                    let dropdown = that.querySelector( Filter.DROPDOWN_QUERY );

                    if( dropdown ){
                        dropdown.value = selectedFilter.getAttribute('data-sscmgrid-filtertab'); //assign filter value
                    }
                }
                

            });

            this.current_filter = null;
            this.has_associated_slick_slider = this.elem.dataset.sscmgridFilterSlider !== undefined;

            // Call the new method to filter on first load
            this.filter_on_first_load();
        }

        filter_on_first_load() {
            // Find the initially active tab 
            const activeTab = this.elem.querySelector(
              ".is-SSCMGrid-filter_tab--active"
            );
      
            if (activeTab) {
              // Trigger the filter logic for the active tab
              this.filter_intent(activeTab, new Event("auto-filter"));
            }
        }

        update_filter_condition() {
            var $elem;

            if (this.has_associated_slick_slider) {
                //We don't enqueue with a dependency on jQuery or Slick, so we
                //can't bind to it with IIFE parameters nor can we depend on
                //this.$elem existing.
                //
                //We also don't use the --hidden modifier since it interferes
                //with Slick's own filtering mechanisms.
                $elem = window.jQuery(this.slider);
                $elem.slick("slickUnfilter");
                
                if (this.current_filter !== null) {
                    $elem.slick("slickFilter", (index, fe_elem) => {
                        var item_categories = fe_elem.dataset.sscmgridItemcategories.split(",").map((c) => c.trim());
                        return item_categories.indexOf(this.current_filter) !== -1;
                    });
                }
            } else {
                this.items.forEach((i) => {
                    var item_categories = i.dataset.sscmgridItemcategories.split(",").map((c) => c.trim());
    
                    i.classList.toggle("is-SSCMGrid-grid_item--hidden", this.current_filter !== null && item_categories.indexOf(this.current_filter) === -1);
                });
            }

            this.tabs.forEach((t) => {
                t.classList.toggle("is-SSCMGrid-filter_tab--active", this.current_filter === t.dataset.sscmgridFiltertab.trim())
            })
        }

        filter_intent(filter_tab, evt) {
            var target_category = filter_tab.dataset.sscmgridFiltertab.trim(),
                is_all = filter_tab.dataset.hasOwnProperty("sscmgridFiltertabAll");

            evt.preventDefault();

            if (this.current_filter === target_category || is_all) {
                this.current_filter = null;
            } else {
                this.current_filter = target_category;
            }

            this.update_filter_condition();
        }
    }

    Behaviors.register_behavior(Filter);

    return Filter;
}(window.EVASuit.Behaviors));
//# sourceMappingURL=SSCMGrid-filter.js.map
