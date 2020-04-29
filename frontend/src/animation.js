import { cubicOut } from 'svelte/easing';


export function flyAnimation(node, {
    delay = 200,
    duration = 300,
    easing = cubicOut,
    z = 0,
    level = 1,
}) {
    const style = getComputedStyle(node);
    const opacity = +style.opacity;
    const transform = style.transform === 'none' ? '' : style.transform;
    return {
        delay: delay * level * 1.3 ,
        duration,
        easing,
        css: t => `
			transform: ${transform} matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, ${(1 - t) * z}, 1);
			opacity: ${t * opacity}`
    };
}
