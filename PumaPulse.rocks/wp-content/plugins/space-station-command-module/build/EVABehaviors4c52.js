window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

window.EVASuit.Behaviors.Behavior = function(Element, Document, Behaviors) {
    "use strict";

    /**
     * Determines if an object claims to be a DOM element.
     * 
     * This function is deliberately compatible with DOM elements that are
     * foreign to the current window. False positives are possible if classes
     * exist that have names like Element or HTMLDocument. Such a situation is
     * unlikely.
     * 
     * @param {Object} maybe_elem An object that may or may not be a DOM
     * element
     * 
     * @returns True if the element is a DOM element, regardless of the iframe
     * it was constructed in. False for all other objects.
     */
    function isDomElement(maybe_elem) {
        var proto = maybe_elem.__proto__;

        while (proto) {
            var typeName = Object.prototype.toString.call(proto);

            if (typeName === "[object Element]" || typeName === "[object HTMLDocument]") {
                return true;
            }

            proto = proto.__proto__;
        }

        return false;
    }

    /**
     * Unique name for our list of located instances.
     */
    const LOCATED_INSTANCES = Symbol("locatedInstances");

    /**
     * A custom JavaScript behavior that can be repeatedly located onto a set
     * of elements named by a CSS selector.
     */
    class Behavior {
        /**
         * Find markup that this Behavior locates onto within a given context
         * and instantiate the class on that markup.
         * 
         * The current class's QUERY parameter will be used as the CSS selector
         * to find markup with. If the given context itself also matches the
         * selector, it 
         * 
         * @param {jQuery|Element|null} context The context element to find
         * markup in. If null, the current document is checked.
         * @param {...any} _ Any arguments to pass on down into the context.
         * 
         * Must either be shaped like a jQuery object or a DOM element.
         */
        static find_markup(context=null) {
            var results = [], i, splitArgs = [], Class = this, nodelist;

            function processElem(index, elem) {
                var locateArgs = [elem].concat(splitArgs);

                results.push(Class.locate.apply(Class, locateArgs));
            }

            for (i = 1; i < arguments.length; i += 1) {
                splitArgs.push(arguments[i]);
            }

            if (context === null) {
                context = document;
            }

            if (isDomElement(context)) { //Element-like context
                nodelist = Array.prototype.slice.call(context.querySelectorAll(Class.QUERY));
                nodelist.forEach(element => {
                    processElem(undefined, element);
                });

                //Documents lack a matches method
                if (context.matches && context.matches(Class.QUERY)) {
                    processElem(undefined, context);
                }
            } else if (context.filter && context.find) { //jQuery-like context
                context.filter(Class.QUERY).each(processElem);
                context.find(Class.QUERY).each(processElem);
            } else {
                throw new Behaviors.ElementMissingError("Behavior.find_markup called without valid context object");
            }
        }
        
        /**
         * Instantiate this Behavior onto this element.
         * 
         * Behaviors are designed to locate onto a given element once and only
         * once. If it has already been instantiated, then that instance will
         * be returned again.
         * 
         * @param {jQuery|Element} elem The element to locate on.
         * 
         * May either be a DOM element or jQuery.
         * 
         * @param {...any} objectArgs Any other arguments to pass to the
         * behavior's constructor.
         * 
         * @returns An instance of the Behavior on this element.
         * 
         * @throws ElementMissingError if the element is neither jQuery nor a
         * DOM element, or if it's jQuery but has a length of 0.
         */
        static locate(elem, ...objectArgs) {
            var Class = this, instance;

            if (isDomElement(elem)) { //Element-like element
                if (Class[LOCATED_INSTANCES] === undefined) {
                    Class[LOCATED_INSTANCES] = new WeakMap();
                }

                if (!Class[LOCATED_INSTANCES].has(elem)) {
                    Class[LOCATED_INSTANCES].set(elem, new Class(elem, ...objectArgs));
                }

                return Class[LOCATED_INSTANCES].get(elem);
            } else if (elem !== null && elem.length !== undefined && elem.length > 0) { //jQuery-like element
                return self.locate(elem[0], ...objectArgs);
            } else {
                throw new Behaviors.ElementMissingError("Behavior.locate called without valid element");
            }
        }

        /**
         * Indicates to the class that content was added to the page.
         * 
         * Subclasses that override this function MUST call find_markup on the
         * full context eventually. You may use this function to delay Behavior
         * processing until a later time, but your Behavior must still be able
         * to handle code locating it before that time.
         * 
         * @param {jQuery|Element} context The content that was added to the DOM.
         */
        static content_ready(context) {
            this.find_markup(context);
        }

        /**
         * Indicates to the class that content is about to be removed from the
         * page.
         * 
         * Most Behaviors do not need to worry about content removal; garbage
         * collection will detach any event handlers and reclaim your object as
         * needed. However, things such as animation timers or other global
         * references to the object will keep it live and potentially leak
         * memory or keep rendering things off-screen. Content removal
         * notifications allow tearing down and disposing of such semantic
         * garbage.
         * 
         * Subclasses that need to support tear down upon removal should
         * override the instance method `deinitialize` instead.
         * 
         * @param {jQuery|Element} context The content that was removed from
         * the DOM.
         */
        static content_removal(context) {
            var Class = this, nodelist;

            function deinitialize_elem(elem) {
                var instance = Class.locate(elem);

                instance.deinitialize();
            }

            if (isDomElement(context)) { //DOM contexts
                nodelist = Array.prototype.slice.call(context.querySelectorAll(Class.QUERY));
                nodelist.forEach(deinitialize_elem);

                if (context.matches(Class.QUERY)) {
                    deinitialize_elem(context);
                }
            } else if (context.filter && context.find) { //jQuery-like context
                context.filter(Class.QUERY).each((index, elem) => deinitialize_elem(elem));
                context.find(Class.QUERY).each((index, elem) => deinitialize_elem(elem));
            } else {
                throw new Behaviors.ElementMissingError("Behavior.content_removal called without valid context object");
            }
        }

        /**
         * Construct a new instance of this Behavior.
         * 
         * The given element will be stored in this.elem. If jQuery is loaded,
         * a wrapped jQuery object with the element will be stored in
         * this.$elem.
         * 
         * @param {Element} elem The DOM element being located upon.
         */
        constructor(elem) {
            this.elem = elem;

            if (window.jQuery) {
                this.$elem = window.jQuery(elem);
            }
        }

        /**
         * Tear down any animation timers or other global references to this
         * Behavior.
         */
        deinitialize() {

        }

        /**
         * Called when the Behavior is presented to the user.
         * 
         * Should not be called to programmatically present a Behavior. To do
         * so, call Behaviors.present.
         */
        presented() {

        }

        /**
         * Called when the Behavior is dismissed.
         * 
         * Should not be called to programmatically dismiss a Behavior. To do
         * so, call Behaviors.dismiss.
         */
        dismissed() {

        }
    }

    return Behavior;
}(window.Element, window.Document, window.EVASuit.Behaviors);;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

window.EVASuit.Behaviors.ElementMissingError = function() {
    "use strict";

    /**
     * Error that indicates that a required element is invalid or missing.
     */
    class ElementMissingError extends Error {
        constructor(message) {
            super(message);
            this.name = "ElementMissingError";
        }
    }

    return ElementMissingError;
}();;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

window.EVASuit.Behaviors.Focus = (function() {
    "use strict";

    var module = {}, element_states = new WeakMap();

    /**
     * Make an entire element and its children unfocusable.
     * 
     * Tabindexes will be set to -1 on all elements. Prior existing indexes
     * will be retained and restored when the element is made focusable again.
     * 
     * @param {Element} elem The DOM element to exclude from focus.
     */
    function make_element_unfocusable(elem) {
        var i;

        if (elem.attributes.tabIndex !== undefined && (!element_states.has(elem) || elem.tabIndex !== -1)) {
            element_states.set(elem, elem.tabIndex);
        }

        elem.tabIndex = -1;

        for (i = 0; i < elem.children.length; i += 1) {
            if (elem.children[i]) {
                make_element_unfocusable(elem.children[i]);
            }
        }
    }

    /**
     * Make an entire element and its children focusable.
     * 
     * This presumes that the element was made unfocusable prior. If it hasn't,
     * no change will be made to the element.
     * 
     * @param {Element} elem The DOM element to include back into focus.
     */
    function make_element_focusable(elem) {
        var i;

        if (element_states.has(elem)) {
            elem.tabIndex = element_states.get(elem);
        } else {
            delete elem.tabIndex;
            delete elem.removeAttribute("tabIndex");
        }

        for (i = 0; i < elem.children.length; i += 1) {
            if (elem.children[i]) {
                make_element_focusable(elem.children[i]);
            }
        }
    }

    module.make_element_focusable = make_element_focusable;
    module.make_element_unfocusable = make_element_unfocusable;

    return module;
}());;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

(window.EVASuit.Behaviors.Hooks = function(Behaviors) {
    "use strict";

    /**
     * Manages global hooks for Behaviors.
     * 
     * A global hook is not tied to any specific instance of a Behavior; unlike
     * events. You add hooks to your behavior by adding one as a property of
     * your class, defining it's hook types, and triggering them in your
     * behavior's methods. Third-party code can then hook into your class by
     * attaching to the class's global hooks mechanism.
     * 
     * Hooks are only to be used in cases where you don't particularly care
     * about *which* behavior you are talking to, only that you want to
     * intercept all of them. They are thus distinct from events, which are
     * fired on a specific behavior and can be used to link different, specific
     * behaviors.
     */
    class Hooks {
        constructor() {
            this.hooks = {};
        }

        /**
         * Define a hook name.
         * 
         * @param {string} hook_name The name of the hook to attach to.
         */
        define_hook_type(hook_name) {
            if (!this.hooks.hasOwnProperty(hook_name)) {
                this.hooks[hook_name] = [];
            }
        }
    
        /**
         * An attached hook callback. Can optionally filter the hook's inherent
         * value.
         * 
         * @callback AttachedHook
         * @param {*} value The inherent hook value, which depends on which
         * hook is being attached.
         * 
         * May have already been filtered by a previously installed hook
         * function.
         * 
         * @param {...*} context Any further context values.
         * 
         * These are always the hook's inherent values and cannot be filtered
         * by user code. By convention, the first context value is the hooked
         * Behavior instance.
         * 
         * @returns The filtered value.
         * 
         * Returning `undefined` (either explicitly, or by not having a
         * `return` statement in your function) indicates that your hook does
         * not wish to change the value.
         */
    
        /**
         * Attach to a particular named hook.
         * 
         * @param {string} hook_name The name of the hook to attach to.
         * @param {AttachedHook} impl The instance to be called at hook time.
         * @throws Error if the `hook_name` is invalid.
         */
        attach(hook_name, impl) {
            this.hooks[hook_name].push(impl);
        }

        /**
         * Trigger a given named hook.
         * 
         * @param {string} hook_name The hook to trigger.
         * @param {*} value The hook value, which hook functions will be
         * expected to modify.
         * @param {Behaviors.Behavior} instance The current behavior being
         * hooked.
         * @param {*} * 
         * @returns The hook value, optionally modified by any attached hooks.
         */
        trigger(hook_name, value, instance) {
            var i, new_value, context = [value, instance];
            for (i = 3; i < arguments.length; i += 1) {
                context.push(arguments[i]);
            }
    
            for (i = 0; i < this.hooks[hook_name].length; i += 1) {
                new_value = this.hooks[hook_name][i].apply(this, context);
                if (new_value !== undefined) {
                    context[0] = new_value;
                }
            }
    
            return context[0];
        }
    }

    return Hooks;
}(window.Behaviors));;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

window.EVASuit.Behaviors = (function(module) {
    "use strict";
    var presentation_stack = [], stack_is_locked = false;

    /**
     * Error that indicates that elements were presented or dismissed in ways
     * that are invalid.
     */
    class PresentationLogicError extends Error {
        constructor(message) {
            super(message);
            this.name = "PresentationLogicError";
        }
    }

    /**
     * Present a given item.
     * 
     * Presentation is hierarchial and follows the DOM tree. We maintain a
     * stack of currently-presented elements. Presenting a new element
     * dismisses all prior elements that are *not* parents of the current one.
     * 
     * Clicking, focusing, tabbing, or ESCing out of the presented element
     * automatically dismisses it.
     * 
     * To respond to presentation and dismissal, implement the presented() and
     * dismissed() methods of your Behavior.
     * 
     * @param {Behaviors.Behavior} item A located behavior to present to
     * the user.
     */
    function present(item) {
        var stack_cleaned = false, i;
        
        if (stack_is_locked) {
            throw new PresentationLogicError("Cannot present items recursively.");
        }

        stack_is_locked = true;

        // Dismiss presented elements off the stack until we catch one that is
        // a parent of the item to be presented.
        while (presentation_stack.length > 0 && !stack_cleaned) {
            var iter = item.elem;

            while (iter !== undefined) {
                if (presentation_stack[presentation_stack.length - 1] === iter) {
                    stack_cleaned = true;
                    break;
                }

                iter = iter.parent;
            }

            try {
                presentation_stack.pop().dismissed();
            } catch (e) {
                stack_is_locked = false;
                throw e;
            }
        }
        
        presentation_stack.push(item);
        
        try {
            item.presented();
        } finally {
            stack_is_locked = false;
        }
    }

    /**
     * Dismiss a given item.
     * 
     * All presented children of this item will also be dismissed.
     * 
     * @param {Behaviors.Behavior} [item] A located behavior to dismiss.
     * 
     * If not provided, the last presented item on the stack will be dismissed.
     */
    function dismiss(item) {
        var stack_index, i = 0;
        
        if (stack_is_locked) {
            throw new PresentationLogicError("Cannot dismiss items recursively.");
        }

        if (presentation_stack.length === 0) {
            throw new PresentationLogicError("Cannot dismiss without presenting first.");
        }

        if (item === undefined) {
            stack_index = presentation_stack.length - 1;
            item = presentation_stack[stack_index];
        } else {
            stack_index = presentation_stack.indexOf(item);
        }

        if (stack_index === -1) {
            throw new PresentationLogicError("Cannot dismiss elements that were not presented.");
        }
        
        while (presentation_stack.length > stack_index) {
            try {
                presentation_stack.pop().dismissed();
            } catch (e) {
                stack_is_locked = false;
                throw e;
            }
        }

        stack_is_locked = false;
    }

    /**
     * Present or dismiss an item based on if it is already presented.
     * 
     * @param {Behaviors.Behavior} item A located behavior to toggle.
     */
    function toggle(item) {
        if (presentation_stack.indexOf(item) !== -1) {
            dismiss(item);
        } else {
            present(item);
        }
    }

    document.addEventListener("keyup", function(evt) {
        if (evt.isComposing || evt.keyCode === 229) {
            // Ignore all composition events caused by IMEs (Input Method
            // Editors, used for Chinese, Japanese, Korean, etc) on desktop.
            return;
        }

        if (evt.key === "Esc" || evt.key === "Escape" || evt.keyCode === 27) {
            if (presentation_stack.length > 0) {
                dismiss();
            }
        }
    });

    module.present = present;
    module.dismiss = dismiss;
    module.toggle = toggle;

    return module;
}(window.EVASuit.Behaviors));;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

(function(Behaviors) {
    "use strict";

    var behavior_registry = {},
        content_ready_listeners = [];

    /**
     * Add a class to the behavior registry.
     * 
     * @param {Function} Class A behavior subclass.
     * @param {String} name The name of the class.
     * 
     * Inferred to be the class's QUERY if not provided.
     */
    function register_behavior(Class, name) {
        if (name === undefined) {
            name = Class.QUERY;
        }

        if (behavior_registry[name] === Class) {
            console.warn("Attempted to register the same behavior twice to CSS selector \"" + name + "\"");
            return;
        }

        if (behavior_registry[name] !== undefined) {
            console.error("Attempted to register a second behavior onto CSS selector \"" +
                name + "\". Only one behavior may be registered to a given CSS selector " +
                "at a given time. The offending classes are " + Class.name +
                " and " + behavior_registry[name].name + ".");
            
            return;
        }

        behavior_registry[name] = Class;
    }
    
    /**
     * Register a function that is called when content is added to the page.
     * 
     * This function should only be called for tying external code to the
     * content listener system. For example, Drupal ships its own behaviors
     * system separate from this one; you can use registered listeners to
     * trigger it when Behaviors' registry is pinged.
     * 
     * @param {Function} func The function to call when content is added.
     */
    function register_content_listener(func) {
        content_ready_listeners.push(func);
    }

    /**
     * Indicate that content has been added to the page.
     * 
     * All registered Behaviors will locate any matching elements within the
     * provided content. Each Behavior will be isolated to a separate
     * setTimeout call to prevent breaking the whole page.
     * 
     * If the page has any alternative frameworks that provide the same
     * facility of notifying JS that content has been added to the page, then
     * that facility should be altered to call this function, and this function
     * should be hotpatched to call that facility. See
     * `register_content_listener` for more information.
     * 
     * @param {jQuery|Element} context The content that was added to the page.
     */
    function content_ready(context) {
        var k, i;
        
        function do_later(obj, func) {
            window.setTimeout(func.bind(obj, context), 0);
        }
        
        for (i = 0; i < content_ready_listeners.length; i += 1) {
            do_later(undefined, content_ready_listeners[i]);
        }

        for (k in behavior_registry) {
            if (behavior_registry.hasOwnProperty(k)) {
                do_later(behavior_registry[k], behavior_registry[k].content_ready);
            }
        }
    }

    /**
     * Indicate that content is about to be removed from the page.
     * 
     * This should be called *before* removing the actual elements. Registered
     * Behaviors will stop any animations timers and remove any global
     * references to about-to-be-removed content to prevent it from consuming
     * client resources.
     * 
     * If the page has any alternative frameworks that provide the same
     * facility of notifying JS that content will be removed from the page,
     * then that facility should be altered to call this function, and this
     * function should be hotpatched to call that facility.
     * 
     * @param {jQuery|Element} context The content that was added to the page.
     */
    function content_removal(context) {
        var k, i;
        
        function do_later(obj, func) {
            window.setTimeout(func.bind(obj, context), 0);
        }
        
        for (k in behavior_registry) {
            if (behavior_registry.hasOwnProperty(k)) {
                do_later(behavior_registry[k], behavior_registry[k].content_removal);
            }
        }
    }

    window.document.addEventListener("DOMContentLoaded", function() {
        content_ready(window.document);
    });

    window.addEventListener(
        "message",
        function(event) {
            if (event.data && event.data.EVASuit &&
                event.data.EVASuit.Behaviors &&
                event.data.EVASuit.Behaviors.content_ready) {
                
                let context = document.querySelector(event.data.EVASuit.Behaviors.content_ready);
                content_ready(context);
            }
        }
    )

    Behaviors.register_behavior = register_behavior;
    Behaviors.register_content_listener = register_content_listener;
    Behaviors.content_ready = content_ready;
    Behaviors.content_removal = content_removal;
}(window.EVASuit.Behaviors));;window.EVASuit = window.EVASuit || {};
window.EVASuit.Behaviors = window.EVASuit.Behaviors || {};

window.EVASuit.Behaviors.throttle_single = function() {
    "use strict";
    
    /* Throttle an event handler.
     *
     * Returns a function which, no matter how frequently it's called, will
     * only trigger a maximum of once per timeout period. More specifically,
     * the first event will always be processed, then, no events will process
     * until the end of the timeout period. If one or more events occurred
     * during this period, the last event recieved will trigger immediately
     * after the end of the timeout period, as well as restart the throttling
     * period. Any preceding events will be discarded.
     *
     * Not to be confused with a debounce, which only fires the event handler
     * at the end of a string of events spaced closer than the timeout period.
     *
     * The nature of this function means that any passed in function's return
     * value will be discarded.
     */
    function throttle_single(func, timeout) {
        var lastTimeout, afterLastArgs, afterLastThis;

        function unthrottle() {
            if (afterLastArgs !== undefined) {
                func.apply(afterLastThis, afterLastArgs);
                afterLastArgs = undefined;
                lastTimeout = window.setTimeout(unthrottle, timeout);
            } else {
                lastTimeout = undefined;
            }
        }

        return function () {
            var myThis = this, myArgs = [], i;

            for (i = 0; i < arguments.length; i += 1) {
                myArgs.push(arguments[i]);
            }

            if (lastTimeout === undefined) {
                func.apply(myThis, myArgs);
                lastTimeout = window.setTimeout(unthrottle, timeout);
            } else {
                afterLastArgs = myArgs;
                afterLastThis = myThis;
            }
        };
    }

    return throttle_single;
}();
//# sourceMappingURL=EVABehaviors.js.map
