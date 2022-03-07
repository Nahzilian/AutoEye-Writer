function animateFrom(elem, direction) {
    direction = direction || 1;
    var x = 0,
        y = direction * 400;
    elem.style.transform = "translate(" + x + "px, " + y + "px)";
    elem.style.opacity = "0";
    gsap.fromTo(elem, { x: x, y: y, autoAlpha: 0 }, {
        duration: 1.25,
        x: 0,
        y: 0,
        autoAlpha: 1,
        ease: "expo",
        overwrite: "auto",
    });
}


gsap.registerPlugin(ScrollTrigger);

gsap.utils.toArray(".gs_reveal").forEach(function (elem) {
    ScrollTrigger.create({
        trigger: elem,
        onEnter: function () { animateFrom(elem) },
        once: true,
    });
});