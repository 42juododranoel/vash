const { series, parallel, watch, src, dest } = require('gulp');
const hash = require('gulp-hash');
const sass = require('gulp-sass');
const cleanCSS = require('gulp-clean-css');
const uglify = require('gulp-uglify');
const autoprefixer = require('gulp-autoprefixer');
const rename = require('gulp-rename');
const tap = require('gulp-tap');
const buffer = require('gulp-buffer');
const image = require('gulp-image');
const browserSync = require('browser-sync').create();
const browserify = require('browserify');
const notifier = require('node-notifier');

const config = {};

config.paths = {
    src: {
        scss: 'sources/scss',
        js: 'sources/js',
    },
    dist: {
        css: '/resources/assets/css',
        js: '/resources/assets/js',
        img: '/resources/assets/img'
    }
}

config.browserSync = {
    // proxy: 'localhost:8000'
    open: false,
    server: { baseDir: "./" },
    files: [
        config.paths.dist.css,
        config.paths.dist.js,
        '**/*.html'
    ]
};

const handleError = (err, title) => {
    console.log(err);

    notifier.notify({
        title,
        message: err.message,
        sound: 'Basso'
    });
}

const compileSCSS = () => {
    return src(`${config.paths.src.scss}/styles.scss`)
        .pipe(sass().on('error', err => handleError(err, 'SCSS Compile Error')))
        .pipe(autoprefixer())
        .pipe(cleanCSS({ compatibility: '*' }))
        .pipe(hash())
        .pipe(rename({ suffix: '.min' }))
        .pipe(dest(config.paths.dist.css))
}

const compileJS = () => {
    return src(`${config.paths.src.js}/*.js`, { read: false })
        .pipe(tap(file => {
            file.contents = browserify(file.path, { debug: true })
                .transform('babelify', { presets: ['@babel/preset-env'] })
                .bundle();
        }))
        .pipe(buffer())
        .pipe(uglify().on('error', err => handleError(err, 'JS Compile Error')))
        .pipe(rename({ suffix: '.min' }))
        .pipe(dest(config.paths.dist.js));
}

const optimizeImages = () => {
    return src(`${config.paths.dist.img}/**/*`)
        .pipe(image())
        .pipe(dest(config.paths.dist.img));
}

const liveReload = () => {
    browserSync.init(config.browserSync)
}

const watchForChanges = () => {
    watch(`${config.paths.src.js}/**/*.js`, compileJS)
    watch(`${config.paths.src.scss}/**/*.scss`, compileSCSS)
};

const compileWatch = series(compileSCSS, watchForChanges);
const compileWatchReload = series(compileSCSS, parallel(watchForChanges, liveReload));

const build = series(compileSCSS, compileJS, optimizeImages);

exports.compileSCSS = compileSCSS;
exports.compileJS = compileJS;
exports.optimizeImages = optimizeImages;
exports.liveReload = liveReload;

exports.compileWatch = exports.devNoReload = compileWatch;
exports.compileWatchReload = exports.dev = compileWatchReload;
exports.build = build;
