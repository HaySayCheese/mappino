var gulp        = require('gulp'),
    path        = require('path'),
    del         = require('del'),
    runSequence = require('run-sequence'),
    rename      = require("gulp-rename"),

    less        = require('gulp-less'),
    minifyCSS   = require('gulp-minify-css'),

    uglify      = require('gulp-uglify');



var COMPILED_CSS_FILE_NAME = 'base.min.css';
var PATHS = {
    BUILD: {
        PATH:       './static/build/',
        FONTS:      './static/build/fonts/',
        IMAGES:     './static/build/images/',
        STYLES:     './static/build/styles/',
        VENDORS:    './static/build/vendors/'
    },
    SOURCE: {
        PATH:       './static/source/',
        FONTS:      './static/source/fonts/',
        IMAGES:     './static/source/images/',
        STYLES:     './static/source/styles/',
        VENDORS:    './static/source/vendors/'
    }
};



/** Task Clean: Clean all from build folder **/
gulp.task('Clean', function(cb) {
    del([PATHS.BUILD.PATH + '*'], cb);
});



/** Task Less:Home: Compile 'source/styles/home/base.less' **/
gulp.task('Less:Home', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/home/base.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/home/'));
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
gulp.task('Less', ['Less:Main', 'Less:Home', 'Less:Cabinet']);






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

/** Task Copy:Vendors: Copy vendors to build folder **/
gulp.task('Copy:Vendors', function() {
    gulp.src(PATHS.SOURCE.VENDORS + '/**/*.{js,ts,coffee}')
        .pipe(uglify())
        .pipe(gulp.dest(PATHS.BUILD.VENDORS));
});

/** Task Copy: Run all 'Copy:*' tasks **/
gulp.task('Copy', ['Copy:Fonts', 'Copy:Images', 'Copy:Vendors']);







/** Task Watch:Home: (use 'gulp Watch:Home' to run watchers) **/
gulp.task('Watch:Home', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/home/**', function() {
        gulp.run('Less:Home');
    });
});

/** Task Watch:Main: (use 'gulp Watch:Main' to run watchers) **/
gulp.task('Watch:Home', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/main/**', function() {
        gulp.run('Less:Main');
    });
});

/** Task Watch:Cabinet: (use 'gulp Watch:Cabinet' to run watchers) **/
gulp.task('Watch:Cabinet', function() {
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/**', function() {
        gulp.run('Less:Cabinet');
    });
});







/** default task (use 'gulp' to build project) **/
gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Less'], callback);
});