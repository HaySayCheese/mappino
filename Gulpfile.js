var gulp        = require('gulp'),
    del         = require('del'),
    runSequence = require('run-sequence'),
    rename      = require("gulp-rename"),

    sass        = require('gulp-sass'),
    minifyCSS   = require('gulp-minify-css'),

    ts          = require('gulp-typescript'),

    uglify      = require('gulp-uglify'),
    sourcemaps  = require('gulp-sourcemaps');



var COMPILED_CSS_FILE_NAME = 'base.min.css';
var PATHS = {
    BUILD: {
        PATH:       './static/build/',
        FONTS:      './static/build/fonts/',
        IMAGES:     './static/build/images/',
        ICONS:      './static/build/icons/',
        STYLES:     './static/build/styles/',
        SCRIPTS:    './static/build/scripts/',
        LIBRARIES:  './static/build/libraries/'
    },
    SOURCE: {
        PATH:       './static/source/',
        FONTS:      './static/source/fonts/',
        IMAGES:     './static/source/images/',
        ICONS:      './static/source/icons/',
        STYLES:     './static/source/styles/',
        SCRIPTS:    './static/source/scripts/',
        LIBRARIES:  './static/source/libraries/'
    }
};



/** Task Clean: Clean all from build folder **/
gulp.task('Clean', function(cb) {
    del([PATHS.BUILD.PATH + '*'], cb);
});






/** Task Copy:Fonts: Copy fonts to build folder **/
gulp.task('Copy:Fonts', function() {
    gulp.src(PATHS.SOURCE.FONTS + '/**/*.{ttf,woff,woff2,eot,svg}')
        .pipe(gulp.dest(PATHS.BUILD.FONTS));
});

/** Task Copy:Images: Copy images to build folder **/
gulp.task('Copy:Images', function() {
    gulp.src(PATHS.SOURCE.IMAGES + '/**/*.{png,jpg,jpeg,gif}')
        .pipe(gulp.dest(PATHS.BUILD.IMAGES));
});

/** Task Copy:Libraries: Copy Libs to build folder **/
gulp.task('Copy:Libraries', function() {
    gulp.src(PATHS.SOURCE.LIBRARIES + '/**/*.{js,ts}')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(PATHS.BUILD.LIBRARIES));
});

/** Task Copy: Run all 'Copy:*' tasks **/
gulp.task('Copy', ['Copy:Fonts', 'Copy:Images', 'Copy:Libraries']);







/** Task Sass:Landing: Compile 'source/styles/landing/base.scss' **/
gulp.task('Sass:Landing', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/landing/base.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/landing/'));
});

/** Task Sass:Map: Compile 'source/styles/map/base.scss' **/
gulp.task('Sass:Map', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/map/base.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/map/'));
});

/** Task Sass:Cabinet: Compile 'source/styles/cabinet/base.scss' **/
gulp.task('Sass:Cabinet', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/base.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/'));
});

/** Task Sass: Run all 'Sass:*' tasks **/
gulp.task('Sass', ['Sass:Landing', 'Sass:Map', 'Sass:Cabinet']);







/** Task TypeScript:Landing - Compile 'source/scripts/landing/*' **/
gulp.task('TypeScript:Landing', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/landing/_references.ts')
        .pipe(sourcemaps.init())
        .pipe(ts({
            noImplicitAny: false,
            target: 'ES5',
            sortOutput: true,
            out: 'landing.js'
        }))
        .pipe(uglify())
        .pipe(sourcemaps.write('/'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/landing/'));
});

/** Task TypeScript:Map - Compile 'source/scripts/map/*' **/
gulp.task('TypeScript:Map', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/map/_references.ts')
        .pipe(sourcemaps.init())
        .pipe(ts({
            noImplicitAny: false,
            target: 'ES5',
            sortOutput: true,
            out: 'map.js'
        }))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/map/'));
});

/** Task TypeScript:Map - Compile 'source/scripts/map/*' **/
gulp.task('TypeScript:Cabinet', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/_references.ts')
        .pipe(sourcemaps.init())
        .pipe(ts({
            noImplicitAny: false,
            target: 'ES5',
            sortOutput: true,
            out: 'cabinet.js'
        }))
        .pipe(uglify())
        .pipe(sourcemaps.write('/'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/'));
});

/** Task TypeScript: Run all 'TypeScript:*' tasks **/
gulp.task('TypeScript', ['TypeScript:Landing', 'TypeScript:Map', 'TypeScript:Cabinet']);





gulp.task('watch', function () {
    gulp.watch(PATHS.SOURCE.STYLES + '/_common/**/*.scss',   ['Sass']);
    gulp.watch(PATHS.SOURCE.STYLES + '/map/**/*.scss',       ['Sass:Map']);
    gulp.watch(PATHS.SOURCE.STYLES + '/landing/**/*.scss',   ['Sass:Landing']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/**/*.scss',   ['Sass:Cabinet']);


    gulp.watch(PATHS.SOURCE.SCRIPTS + '/_common/**/*.ts',   ['TypeScript']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/map/**/*.ts',       ['TypeScript:Map']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/landing/**/*.ts',   ['TypeScript:Landing']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/**/*.ts',   ['TypeScript:Cabinet']);
});





/** default task (use 'gulp' to build project) **/
gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Sass', 'TypeScript'], callback);
});