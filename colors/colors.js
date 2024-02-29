

function run() {
    const paletteType = document.getElementById("palette-type");
    gen();

    paletteType.addEventListener("input", function () {
        gen();
    });
}

function gen() {
    const paletteType = document.getElementById("palette-type");
    const colorInputOne = document.getElementById("color1");
    const blindnessMode = document.getElementById("color-blindness");
    const colorInputTwo = document.getElementById("color2");
    const paletteCount = document.getElementById("palette-count-input");

    switch (paletteType.value) {
        case "sequential":
            generateSequential([black_fix(colorInputOne.value), black_fix(colorInputTwo.value)], paletteCount.value, blindnessMode.value);

            [colorInputOne, colorInputTwo, paletteCount, blindnessMode].forEach((colorInput) => {
                colorInput.addEventListener("input", function () {
                    generateSequential([black_fix(colorInputOne.value), black_fix(colorInputTwo.value)], paletteCount.value, blindnessMode.value);
                });
            });
            break;

        case "triad":
            generateEquidistance(black_fix(colorInputOne.value), 3, blindnessMode.value);

            [colorInputOne, colorInputTwo, blindnessMode].forEach((colorInput) => {
                colorInput.addEventListener("input", function () {
                    generateEquidistance(black_fix(colorInputOne.value), 3, blindnessMode.value);
                });
            });
            break;

        case "spectrum":
            generateEquidistance(black_fix(colorInputOne.value), black_fix(paletteCount.value), blindnessMode.value);

            [colorInputOne, colorInputTwo, paletteCount, blindnessMode].forEach((colorInput) => {
                colorInput.addEventListener("input", function () {
                    generateEquidistance(black_fix(colorInputOne.value), paletteCount.value, blindnessMode.value);
                });
            });
            break;

        case "diverging":
            generateDiverging(black_fix(colorInputOne.value), black_fix(colorInputTwo.value), paletteCount.value, blindnessMode.value);

            [colorInputOne, colorInputTwo, paletteCount, blindnessMode].forEach((colorInput) => {
                colorInput.addEventListener("input", function () {
                    generateDiverging(black_fix(colorInputOne.value), black_fix(colorInputTwo.value), paletteCount.value, blindnessMode.value);
                });
            });
            break;
    }
}

// blue shifted ought to be darker shifted and yellow shifted ligher shifted
function generateEquidistance(col, splits, blindnessMode) {
    let colors = Array.from({ length: splits }, (_, i) => {
        return chroma(col).set('oklch.h', '+' + (i * (360 / splits)).toString());
    });

    createPanels(colors, blindnessMode)
}

function generateSequential(cols, paletteCount, blindnessMode) {
    const colors = chroma.scale(cols).mode("oklch").colors(paletteCount);
    console.log(blindnessMode);

    createPanels(colors, blindnessMode);

    color_strings = colors.map(s => s.replace(/^#/, "0x"))
    console.log("[" + color_strings.join(", ") + "]");
}

function generateDiverging(col1, col2, paletteCount, blindnessMode) {
    col1 = chroma(chroma(col1).oklch());
    col2 = chroma(chroma(col2).oklch());

    let brightness = (chroma(col1).get('oklch.l')); // ((chroma(col1).get('oklch.l')) + (chroma(col2).get('oklch.l'))) / 2;// (parseFloat(chroma(col1).get('oklch.l')) + parseFloat(chroma(col2).get('oklch.l'))) / 2
    console.log(brightness, chroma(col1).get('oklch.l'), chroma(col2).get('oklch.l'))
    let sat = (chroma(col1).get('oklch.c')); // (chroma(col1).get('oklch.c') + chroma(col2).get('oklch.c')) / 2;
    console.log(sat, chroma(col1).get('oklch.c'), chroma(col2).get('oklch.c'))
    let bright_diff = chroma("white").get('oklch.l') - brightness;
    let sat_diff = chroma("white").get('oklch.c') - sat;
    let new_col1 = chroma(col1).set('oklch.c', sat).set('oklch.l', brightness);
    let new_col2 = chroma(col2).set('oklch.c', sat).set('oklch.l', brightness);

    let new_col1_dark = new_col1.set('oklch.l', Math.min(Math.max(0, brightness - bright_diff)), 1)
        .set('oklch.c', Math.min(Math.max(0, sat - sat_diff), 1));

    let new_col2_dark = new_col2.set('oklch.l', Math.min(Math.max(0, brightness - bright_diff)), 1)
        .set('oklch.c', Math.min(Math.max(0, sat - sat_diff), 1));

    let new_col1_light = new_col1.set('oklch.l', Math.min(Math.max(0, brightness + bright_diff)), 1)
        .set('oklch.c', Math.min(Math.max(0, sat + sat_diff), 1));


    let new_col2_light = new_col2.set('oklch.l', Math.min(Math.max(0, brightness + bright_diff)), 1)
        .set('oklch.c', Math.min(Math.max(0, sat + sat_diff), 1));

    const colors = chroma.scale([new_col1, chroma("white"), new_col2]).mode("oklch").colors(paletteCount);

    createPanels(colors, blindnessMode)
}

function createPanels(colors, blindnessMode) {
    const palettes = document.getElementById("palette");
    palettes.innerHTML = "";

    colors.forEach((color) => {
        const panel = document.createElement("div");
        const colorDisplay = document.createElement("span");
        colorDisplay.classList.add("color-display");

        const contrastColor = chroma.contrast(color, chroma(color).darken(3));
        const textColor = contrastColor > 2 ? chroma(color).darken(3) : chroma(color).luminance(3);

        panel.style.setProperty("--text-color", textColor);
        colorDisplay.appendChild(document.createTextNode(color));
        panel.appendChild(colorDisplay);

        panel.classList.add("panel");
        panel.style.setProperty("--palette-color", colorBlindSim(color, blindnessMode));
        palettes.appendChild(panel);
    });
}

// Gradients just don't work well with pure black
function black_fix(col) {
    if (col == "#000000") {
        return "#010101";
    } else {
        return col;
    }
}

window.addEventListener("load", run);
