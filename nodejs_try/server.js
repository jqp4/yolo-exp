// Подключегние внешний модулей, которые находятся в node_modules
const path = require("path");
const fs = require("fs");
const Koa = require("koa");
const serve = require("koa-static");
const Router = require("@koa/router");
const multer = require("@koa/multer");
const cors = require("@koa/cors");
const { spawn } = require("child_process");
const koaStatic = require("koa-static");

const app = new Koa();
const router = new Router();

// порт на котором откроется сервер
const PORT = 3001;

// задаем имя папке для скачивания файлов
// __dirname - папка, откуда запустили этот скрипт. у нас это корень
const UPLOAD_DIR = path.join(__dirname, "/uploadFiles");

// статус обработки загруженного файла
var uploadedFileProcessing = {
    inProgress: null,
};

// todo
// let uploadingStatus = uploadedFileProcessing.done;
// const uploadedFileProcessing = {
//     inProgress: 1,
//     error: 2,
//     done: 3,
// };

// Routing
// роутеру приходят запросы от клиента, что пользователь
// хочет перейти на какоую-то страницу по заданному адресу
router.get("/", (ctx, next) => {
    ctx.type = "html";

    ctx.body = fs.createReadStream(
        path.join(__dirname, "public", "/algoviewCodeCopy/AlgoView.html")
    );

    next();
});

router.get("/fileUpload", (ctx, next) => {
    ctx.type = "html";

    if (uploadedFileProcessing.inProgress) {
        ctx.body = "Uploaded file processing in progress ...";
        return next();
    }

    ctx.body = fs.createReadStream(
        path.join(__dirname, "public", "/fileUpload.html")
    );

    next();
});

// File Uploading
// пока пропустил
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, UPLOAD_DIR);
    },
    filename: function (req, file, cb) {
        cb(null, `${file.originalname}`);
    },
});

const upload = multer({ storage: storage });

// add a route for uploading single files
router.post("/upload-single-file", upload.single("file"), (ctx) => {
    // Run python script
    var dataToSend;

    // spawn new child process to call the python script
    const shScript = spawn("sh", [
        "scripts/run.sh",
        // UPLOAD_DIR, // путь к файлу
        // ctx.request.file.filename, // имя файла
        UPLOAD_DIR + "/" + ctx.request.file.filename,
    ]);

    uploadedFileProcessing.inProgress = true;

    // collect data from script
    const collectData = function (data) {
        // console.log("Pipe data from python script ...");
        // dataToSend = data.toString();
        // console.log(data.toString());
    };

    shScript.stdout.on("data", collectData);
    shScript.stderr.on("data", collectData);

    // in close event we are sure that stream from child process is closed
    shScript.on("close", (code) => {
        console.log(`child process close all stdio with code ${code}`);
        console.log(dataToSend);

        uploadedFileProcessing.inProgress = false;
    });

    ctx.body = {
        uploadStatus: `file ${ctx.request.file.filename} has been saved on the server`,
        url: `http://localhost:${PORT}/${ctx.request.file.originalname}`,
    };
});

// подключаем стили и мои дополнительные модули к THREE
app.use(koaStatic(path.join(__dirname, "public/algoviewCodeCopy")));

app.use(cors());
app.use(router.routes()).use(router.allowedMethods());
app.use(serve(UPLOAD_DIR));

app.listen(PORT, () => {
    console.log(`app starting at port ${PORT}`);
});
