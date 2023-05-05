const sharp = require("sharp");

IMAGE_SIZE = 10;

function main() {
    sharp("uploadFiles/test4.jpg")
        .resize(IMAGE_SIZE, IMAGE_SIZE, {
            fit: sharp.fit.fill,
        })
        .toFile("uploadFiles/output.png", (err, info) => {})

        .toBuffer()
        .then((data) => {
            const pixelArray = new Uint8ClampedArray(data.buffer);

            console.log(
                pixelArray,
                IMAGE_SIZE * IMAGE_SIZE * 3,
                data.length,
                data.BYTES_PER_ELEMENT
            );

            // for (let num of data) {
            //     // process.stdout.write(num);
            //     // process.stdout.write(" ");
            //     console.log(num);
            // }

            let outputArray = Float32Array.from(
                { length: data.length },
                (_, i) => data[i] // / 255
            );

            console.log(outputArray);
        });
}

main();
