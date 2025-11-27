window.SpaceStation = window.SpaceStation || {};
window.SpaceStation.CommandModule = window.SpaceStation.CommandModule || {};
window.SpaceStation.CommandModule.Slider = window.SpaceStation.CommandModule.Slider || {};

window.SpaceStation.CommandModule.Slider.Tab = (function($, Behaviors, module) {
    class Tab extends Behaviors.Behavior {
        static QUERY = "[data-sscmslider-tab]"

        static PARENT_QUERY = "[data-sscmslider]";
        static SLIDER_QUERY = "[data-sscmslider-contentrow]";

        constructor(...args) {
            super(...args)

            this.parent = this.elem.closest(Tab.PARENT_QUERY);
            this.slider = this.parent.querySelector(Tab.SLIDER_QUERY);
            this.tabs = module.Tabs.locate(this.elem.closest(module.Tabs.QUERY));

            this.$slider = $(this.slider);

            this.target = parseInt(this.elem.dataset.sscmsliderTab);
            this.currentSlide = 0;
            
            this.elem.addEventListener("touchend", this.click_intent.bind(this));
            this.elem.addEventListener("click", this.click_intent.bind(this));

            this.$slider.on("afterChange", this.slide_change_intent.bind(this));

            try {
                this.slide_change_intent(null, this.$slider.slick("getSlick"), this.$slider.slick("slickCurrentSlide"));
            } catch (e) {
                // Catch and report errors when sending initial slide change event
                // to ourselves. This can happen if the load order is wrong.
                // We have to catch the error otherwise all but the first tab breaks.
                console.error("Error when setting up slider tab: " + e);
            }
        }

        click_intent(e) {
            e.preventDefault();
            e.stopPropagation();
            this.tabs.expand_contract_intent();
            this.$slider.slick("slickGoTo", this.target);

            //Tell our tab container that we're about to change the slide.
            //It also listens to afterChange, but that's visibly too late, and
            //for some reason beforeChange is very bugged
            this.tabs.slide_change_intent(null, null, this.target);
        }

        slide_change_intent(event, slick, currentSlide) {    

            let slider = slick.$slider[0];
        
            if( slider.hasAttribute('data-slider-wrapper') ){
                //check if slider is a child
                if( slider.getAttribute('data-slider-wrapper') === "child" ){

                    let tabsContainer = slider.parentNode.querySelector('.SSCMSlider-tabs_content'); // find tabs container

                    if( tabsContainer ){
                       
                            // apply states to child tabs
                            // this is only executed once so we need to scan all tab buttons and manually change states

                            let tabButtons = tabsContainer.querySelectorAll('[data-sscmslider-tab]');

                            tabButtons.forEach( (tab) => {
                                tab.classList.toggle("is-SSCMSlider-tab--active", tab.getAttribute('data-sscmslider-tab') == currentSlide.toString());
                            }); 
                    }
                                        
                    
                    
                    return;
                    
                }
                    

            }
            
            this.currentSlide = currentSlide;

            this.elem.classList.toggle("is-SSCMSlider-tab--active", currentSlide === this.target);
        }
    }

    Behaviors.register_behavior(Tab);

    return Tab;
}(window.jQuery, window.EVASuit.Behaviors, window.SpaceStation.CommandModule.Slider));window.SpaceStation = window.SpaceStation || {};
window.SpaceStation.CommandModule = window.SpaceStation.CommandModule || {};
window.SpaceStation.CommandModule.Slider = window.SpaceStation.CommandModule.Slider || {};

window.SpaceStation.CommandModule.Slider.Tabs = (function($, Behaviors) {
    class Tabs extends Behaviors.Behavior {
        static QUERY = "[data-sscmslider-tabs]"

        static PARENT_QUERY = "[data-sscmslider]";
        static SLIDER_QUERY = "[data-sscmslider-contentrow]";
        static CONTENT_QUERY = "[data-sscmslider-tabscontent]"
        static TAB_QUERY = "[data-sscmslider-tab]"

        constructor(...args) {
            super(...args)

            this.parent = this.elem.closest(Tabs.PARENT_QUERY);
            this.slider = this.parent.querySelector(Tabs.SLIDER_QUERY);
            this.tabs = this.elem.querySelectorAll(Tabs.TAB_QUERY);
            this.tabs_content = this.elem.querySelector(Tabs.CONTENT_QUERY);

            this.mode = this.elem.dataset.sscmsliderTabs;
            this.is_expanded = this.mode !== "dropdown";
            this.currentSlide = 0;

            window.addEventListener("resize", this.relayout_intent.bind(this));

            //Since this is a custom Slick event, we need jQuery to listen to it
            $(this.slider).on("afterChange", this.slide_change_intent.bind(this));

            this.relayout_intent();
            this.set_css_states();
        }

        set_css_states() {
            this.elem.classList.toggle("is-SSCMSlider-tabs--expanded", this.is_expanded);

            if (this.tabs[this.currentSlide] !== undefined) {
                this.elem.scroll({top: this.tabs[this.currentSlide].offsetTop});
            }
        }

        relayout_intent() {
            var i, measured_height = this.tabs_content.offsetHeight, measured_tab_height = 0;

            for (i = 0; i < this.tabs.length; i += 1) {
                measured_tab_height = Math.max(measured_tab_height, this.tabs[i].offsetHeight);
            }
            this.parent.style.setProperty("--SSCMSlider-tabs_content--expanded_height", measured_height + "px")
            this.parent.style.setProperty("--SSCMSlider-tabs_content--collapsed_height", measured_tab_height + "px")
        }

        /**
         * Triggered when an individual tab is clicked.
         */
        expand_contract_intent() {
            if (this.mode === "dropdown") {
                this.is_expanded = !this.is_expanded;
                this.set_css_states();
            }
        }

        /**
         * Triggered when the slide changes.
         * 
         * Sometimes called by Tab behavior; in that case event and slick will
         * be null.
         */
        slide_change_intent(event, slick, currentSlide) {
            this.currentSlide = currentSlide;
            this.set_css_states();
        }

    }

    Behaviors.register_behavior(Tabs);

    return Tabs;
}(window.jQuery, window.EVASuit.Behaviors))
//# sourceMappingURL=SSCMSlider.js.map
