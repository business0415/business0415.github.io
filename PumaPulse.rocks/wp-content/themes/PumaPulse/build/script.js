(function($){
    $(function(){
        if($('body').hasClass('page-bg-animation') && $('body').hasClass('page')){
            if(!$('.BackgroundAnimationMain').length){
                const stars = 
                    `<div class="BackgroundAnimation-stars">
                        <div id="stars-group-1"></div>
                        <div id="stars-group-2"></div>
                        <div id="stars-group-3"></div>
                        <div id="stars-group-4"></div>
                        <div id="stars-group-5"></div>
                        <div id="stars-group-6"></div>
                    </div>`;
                const shootingStars = 
                        `<div class="BackgroundAnimation-shooting_stars shooting-stars">
                            <section>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                            </section>
                        </div>`;
                $('body').append('<div class="BackgroundAnimationMain"></div>');
                $('.BackgroundAnimationMain').append(stars);
                $('.BackgroundAnimationMain').append(shootingStars);
            }
        }
    });
})(jQuery);;(function ($) {
  $(function () {
    // console.log(x, y);
    // const button = document.querySelector(".Btn a");

    // button.addEventListener("mousemove", (e) => {
    //     console.log(button);
    //     const { x, y } = button.getBoundingClientRect();
    //     button.style.setProperty("--x", e.clientX - x);
    //     button.style.setProperty("--y", e.clientY - y);
    // })

    // on page load

    $(window).load(function () {
      attachHoverEffect();
    });

    // on Gravity Forms ajax-enabled multi-page forms
    $(document).on("gform_page_loaded", function (event, formId, currentPage) {
      attachHoverEffect();
    });

    function attachHoverEffect() {
      $(
        ".Btn a, .SinglePrimaryBTN a, .SingleSecondaryBTN a, .DualBtn a, .DualBtnLight a, .gform_button, .gform-button, .gform-theme-button, .SSCMBtn-secondary .SSCMBasePostFeed-post_cta_wrapper"
      ).on("mousemove", function (e) {
        const button = this;
        const rect = this.getBoundingClientRect();

        button.style.setProperty("--x", e.clientX - rect.x);
        // button.style.setProperty("--y", e.clientY - rect.y);
      });
    }
    // $('.Btn a').hover(function(e){
    //     // console.log(this);
    //     const button = this;
    //     const { x, y } = button.getBoundingClientRect();
    //     button.style.setProperty("--x", e.clientX - x);
    //     button.style.setProperty("--y", e.clientY - y);
    // });
  });
})(jQuery);
;jQuery(document).ready(function($) {

    // Hide all pages except first on load
    // $('.gform_page').hide();
    // $('.gform_page').first().show();

    // check if first page is visible and hide progress bar if it is
    // if ($('.ProjectCalculator .gform_page').first().is(':visible')) {
    //     $('.ProjectCalculator .gf_progressbar').removeClass('visible');
    //     console.log('First page is visible, hiding progress bar');
    // } else {
    //     $('.ProjectCalculator .gf_progressbar').addClass('visible');
    // }

    // Add smooth transition to steps via CSS
    // $('<style>.gf_step_transition{transition:background 0.3s, color 0.3s;} .gf_progressbar_percentage{transition:width 0.3s;}</style>').appendTo('head');

    // Target Gravity Forms multipage navigation buttons
    $(document).on('click', '.ProjectCalculator_wrapper .gform_next_button, .ProjectCalculator_wrapper  .gform_previous_button', function(e) {
        e.preventDefault();

        let $form = $(this).closest('form');
        let $currentPage = $form.find('.gform_page:visible');
        let isNext = $(this).hasClass('gform_next_button');
        let $pages = $form.find('.gform_page');
        let currentIndex = $pages.index($currentPage);
        let targetIndex = isNext ? currentIndex + 1 : currentIndex - 1;

        // Validate page if next
        if (isNext && typeof window.gf_check_field_rules === 'function') {
            if (!$form.data('gf_validated')) {
                $form.submit();
                return;
            }
        }

        // Check for errors before progressing (client-side only)
        if (isNext && $form.find('.gfield_error').length > 0) {
            return;
        }

        // Check if all radio groups in the current page have a checked value
        if (isNext) {
            let radiosValid = true;
            $currentPage.find('.gfield_radio').each(function() {
                // Only check visible radio groups
                if ($(this).is(':visible')) {
                    let name = $(this).find('input[type="radio"]').attr('name');
                    if (name && $currentPage.find('input[type="radio"][name="' + name + '"]:checked').length === 0) {
                        radiosValid = false;
                    }
                }
            });
            if (!radiosValid) {
                // Optionally show a message here
                // alert('Please select an option for all required questions.');
                return;
            }
        }

        // check if first page is visible and hide progress bar if it is
        // if (currentIndex === 0 && isNext) {
        //     $('.ProjectCalculator .gf_progressbar').removeClass('visible');
        // } else {
        //     $('.ProjectCalculator .gf_progressbar').addClass('visible');
        // }
    
        // Animate out current page
        $currentPage.fadeOut(300, function() {
            $pages.eq(targetIndex).fadeIn(300);

            updateProgressBar($form.attr('id').replace('gform_', ''), targetIndex + 1);
        });
        $pages.eq(targetIndex).find('.ginput_container').css({
            'opacity': .6,
            'pointerEvents': 'none'
        });
        $pages.eq(targetIndex).find('.gform-page-footer').css({
            'opacity': .6,
            'pointerEvents': 'none'
        });
    });

    $(document).on('click', '.ProjectCalculator_wrapper button[type=submit]', function(e) {
        $(this).addClass('loading');
        $form = $(this).closest('form');
        $form.find('.ginput_container').css({
            'opacity': .6,
            'pointerEvents': 'none'
        });
        $(this).closest('.gform-page-footer').css({
            'opacity': .6,
            'pointerEvents': 'none'
        });
    });

    function updateProgressBar(formId, currentPage) {
        var $form = $('#gform_' + formId);
        var $progressBar = $form.find('.gf_progressbar');
        if ($progressBar.length) {
            var $pages = $form.find('.gform_page');
            var targetIndex = currentPage - 1;
            var percent = ((targetIndex + 1) / $pages.length) * 100;
            $progressBar.find('.gf_progressbar_percentage')
                .css({ transition: 'width 0.3s' })
                .width(percent + '%');
        }
    }
});
;jQuery(document).ready(function ($) {
  // Select all video wrappers that might have your custom button
  const $videoModules = $(".fl-module-video.styled-video");

  $videoModules.each(function () {
    const $module = $(this);
    const $videoWrapper = $module.find(".fl-wp-video .wp-video");
    const videoElement = $videoWrapper.find("video")[0];
    const $customPlayButton = $videoWrapper.find(".custom-video-play-button");
    const isMejsActive = $videoWrapper.find(".mejs-container").length > 0;

    if (videoElement && !isMejsActive && $customPlayButton.length) {
      // ONLY apply custom behavior to single videos without MEJS
      
      // Function to update the 'playing' class based on video state
      const updatePlayingClass = () => {
        if (!videoElement.paused && !videoElement.ended) {
          $videoWrapper.addClass("playing");
        } else {
          $videoWrapper.removeClass("playing");
        }
      };

      // Initial check for autoplay or preloaded state
      updatePlayingClass();
        
      // Handle custom play button clicks
      $customPlayButton.on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        if (videoElement.paused || videoElement.ended) {
          videoElement.play().catch(function (error) {
            console.log("Error playing video:", error);
          });
        }
      });

      // Handle video clicks for pausing
      $(videoElement).on("click", function (e) {
        // Only handle pause if video is playing
        if (!videoElement.paused && !videoElement.ended) {
          e.preventDefault();
          e.stopPropagation();
          videoElement.pause();
        }
      });

      // Update cursor
      const updateCursor = () => {
        if (videoElement.paused || videoElement.ended) {
          $(videoElement).css("cursor", "default");
        } else {
          $(videoElement).css("cursor", "pointer");
        }
      };

      $(videoElement).on("play pause ended", updateCursor);
      updateCursor(); // Initial state

      // Native video event listeners (ONLY for single videos without MEJS)
      $(videoElement).on("play", updatePlayingClass);
      $(videoElement).on("pause", updatePlayingClass);
      $(videoElement).on("ended", updatePlayingClass);
      $(videoElement).on("loadedmetadata", updatePlayingClass);
    }
    
    // For multiple videos with MEJS - do absolutely nothing
    // Let MEJS handle everything completely
  });
});
;(function() {
    function check_for_splines_to_unload() {
        document.querySelectorAll("spline-viewer").forEach((splineViewer) => {
            // Check to see if the spline player is off the page and, if so, unload it.
            let rect = splineViewer.getBoundingClientRect();

            // We consider anything within 150px of the window scroll rect to
            // be potentially visible, in order to force loading to happen
            // sooner during scroll
            let scrollTop = -150;
            let scrollBottom = window.innerHeight + 150;
            if (rect.top < scrollTop && scrollTop < rect.bottom
                || rect.top < scrollBottom && scrollBottom < rect.bottom
                || scrollTop < rect.top && rect.top < scrollBottom
                || scrollTop < rect.bottom && rect.bottom < scrollBottom) {
                
                // Spline viewer is in view.
                if (!splineViewer._loaded) {
                    splineViewer.load();
                }
            } else if (splineViewer._loaded) {
                // Spline viewer is NOT in view.
                splineViewer.unload();
            }
        });
    }

    function throttle(handler) {
        let last_timestamp = performance.now();

        function throttled_handler() {
            let this_timestamp = performance.now();
            if (this_timestamp - last_timestamp > 100) {
                last_timestamp = this_timestamp;

                return handler.apply(this, arguments);
            }
        }

        return throttled_handler;
    }

    window.addEventListener("resize", check_for_splines_to_unload);
    window.addEventListener("scroll", throttle(check_for_splines_to_unload));
    check_for_splines_to_unload();
}());
//# sourceMappingURL=script.js.map
