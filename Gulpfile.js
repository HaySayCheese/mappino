var gulp        = require('gulp'),
    path        = require('path'),
    del         = require('del'),
    runSequence = require('run-sequence'),
    rename      = require("gulp-rename"),

    less        = require('gulp-less'),
    minifyCSS   = require('gulp-minify-css'),

    typeScript  = require('typescript-compiler'),

    ngAnnotate  = require('gulp-ng-annotate'),

    uglify      = require('gulp-uglify'),
    merge       = require('merge2');



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
        LIBRARIES:  './static/source/libs/'
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
        .pipe(uglify())
        .pipe(gulp.dest(PATHS.BUILD.LIBRARIES));
});

/** Task Copy: Run all 'Copy:*' tasks **/
gulp.task('Copy', ['Copy:Fonts', 'Copy:Images', 'Copy:Libs']);








/** Task Less:Home: Compile 'source/styles/home/base.less' **/
gulp.task('Less:Home', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/home/base.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/home/'));
});

/** Task Less:Offer: Compile 'source/styles/offer/base.less' **/
gulp.task('Less:Offer', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/offer/base.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/offer/'));
});

/** Task Less:Main: Compile 'source/styles/main/base.less' **/
gulp.task('Less:Main', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/main/base.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/main/'));
});

/** Task Less:Cabinet: Compile 'source/styles/cabinet/base.less' **/
gulp.task('Less:Cabinet', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/base.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/'));
});

/** Task Less: Run all 'Less:*' tasks **/
gulp.task('Less', ['Less:Main', 'Less:Home', 'Less:Offer', 'Less:Cabinet']);







///** Task TypeScript:Common - Compile 'source/scripts/common/*' **/
//gulp.task('TypeScript:Common', function() {
//    typeScript.compile(['static/source/scripts/common/**/*.ts'], ['--out', 'static/source/scripts/common/']);
//});
//
//






/** Task Watch:Less:Home - (use 'gulp Watch:Home' to run watchers) **/
gulp.task('Watch:Less:Home', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/home/**', function() {
        gulp.run('Less:Home');
    });
});

/** Task Watch:Less:Main - (use 'gulp Watch:Main' to run watchers) **/
gulp.task('Watch:Less:Main', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/main/**', function() {
        gulp.run('Less:Main');
    });
});

/** Task Watch:Less:Cabinet - (use 'gulp Watch:Cabinet' to run watchers) **/
gulp.task('Watch:Less:Cabinet', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/**', function() {
        gulp.run('Less:Cabinet');
    });
});










/** default task (use 'gulp' to build project) **/
gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Less'], callback);
});