var gulp        = require('gulp'),
    del         = require('del'),
    runSequence = require('run-sequence'),
    rename      = require("gulp-rename"),
    concat      = require('gulp-concat'),

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
        STYLES:     './static/build/styles/',
        SCRIPTS:    './static/build/scripts/',
        LIBRARIES:  './static/build/libs/'
    },
    SOURCE: {
        PATH:       './static/source/',
        FONTS:      './static/source/fonts/',
        IMAGES:     './static/source/images/',
        STYLES:     './static/source/styles/',
        SCRIPTS:    './static/source/scripts/',
        LIBRARIES:  './static/source/scripts/libs/'
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

/** Task Copy:Libs: Copy Libs to build folder **/
gulp.task('Copy:Libs', function() {
    gulp.src(PATHS.SOURCE.LIBRARIES + '/**/*.{js,ts,coffee}')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(PATHS.BUILD.LIBRARIES));
});

/** Task Copy: Run all 'Copy:*' tasks **/
gulp.task('Copy', ['Copy:Fonts', 'Copy:Images', 'Copy:Libs']);







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

/** Task Sass: Run all 'Sass:*' tasks **/
gulp.task('Sass', ['Sass:Landing', 'Sass:Map']);







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
        .pipe(sourcemaps.write('/'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/map/'));
});

/** Task TypeScript: Run all 'TypeScript:*' tasks **/
gulp.task('TypeScript', ['TypeScript:Landing', 'TypeScript:Map']);










/** default task (use 'gulp' to build project) **/
gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Sass', 'TypeScript'], callback);
});