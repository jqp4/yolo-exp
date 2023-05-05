const sharp = require("sharp");

IMAGE_SIZE = 640;

function main() {
    sharp("uploadFiles/test1.jpeg")
        .resize(IMAGE_SIZE, IMAGE_SIZE, {
            fit: "fill",
        })
        .toFile("uploadFiles/output.png", (err, info) => {});
}

main();
