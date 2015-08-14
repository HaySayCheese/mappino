var gulp        = require('gulp'),
    del         = require('del'),
    bump        = require('gulp-bump'),

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



gulp.task('Clean', function(cb) {
    del([PATHS.BUILD.PATH + '*'], cb);
});






gulp.task('Copy:Fonts', function() {
    gulp.src(PATHS.SOURCE.FONTS + '/**/*.{ttf,woff,woff2,eot,svg}')
        .pipe(gulp.dest(PATHS.BUILD.FONTS));
});

/** Task Copy:Images: Copy images to build folder **/
gulp.task('Copy:Images', function() {
    gulp.src(PATHS.SOURCE.IMAGES + '/**/*.{png,jpg,jpeg,gif}')
        .pipe(gulp.dest(PATHS.BUILD.IMAGES));
});

gulp.task('Copy:Libraries', function() {
    gulp.src(PATHS.SOURCE.LIBRARIES + '/**/*.{js,ts}')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(PATHS.BUILD.LIBRARIES));
});

gulp.task('Copy', [
    'Copy:Fonts',
    'Copy:Images',
    'Copy:Libraries'
]);







gulp.task('Sass:Landing', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/landing/base.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/landing/'));
});

gulp.task('Sass:Map', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/map/base.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/map/'));
});

gulp.task('Sass:Cabinet:Users', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/users/users.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/users/'));
});

gulp.task('Sass:Cabinet:Moderators', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/moderators/moderators.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename(COMPILED_CSS_FILE_NAME))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/moderators/'));
});

gulp.task('Sass', [
    'Sass:Landing',
    'Sass:Map',
    'Sass:Cabinet:Users',
    'Sass:Cabinet:Moderators'
]);







gulp.task('TypeScript:Landing', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/landing/_all.ts')
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

gulp.task('TypeScript:Map', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/map/_all.ts')
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

gulp.task('TypeScript:Cabinet:Users', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/users/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(ts({
            noImplicitAny: false,
            target: 'ES5',
            sortOutput: true,
            out: 'cabinet.users.js'
        }))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/users/'));
});

gulp.task('TypeScript:Cabinet:Moderators', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/moderators/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(ts({
            noImplicitAny: false,
            target: 'ES5',
            sortOutput: true,
            out: 'cabinet.moderators.js'
        }))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/moderators/'));
});

gulp.task('TypeScript', [
    'TypeScript:Landing',
    'TypeScript:Map',
    'TypeScript:Cabinet:Users',
    'TypeScript:Cabinet:Moderators'
]);






gulp.task('watch', function () {
    gulp.watch(PATHS.SOURCE.STYLES + '/_common/**/*.scss',              ['Sass']);
    gulp.watch(PATHS.SOURCE.STYLES + '/map/**/*.scss',                  ['Sass:Map']);
    gulp.watch(PATHS.SOURCE.STYLES + '/landing/**/*.scss',              ['Sass:Landing']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/users/**/*.scss',        ['Sass:Cabinet:Users']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/moderators/**/*.scss',   ['Sass:Cabinet:Moderators']);


    gulp.watch(PATHS.SOURCE.SCRIPTS + '/core/**/*.ts',                  ['TypeScript']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/map/**/*.ts',                   ['TypeScript:Map']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/landing/**/*.ts',               ['TypeScript:Landing']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/users/**/*.ts',         ['TypeScript:Cabinet:Users']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/moderators/**/*.ts',    ['TypeScript:Cabinet:Moderators']);
});





/** default task (use 'gulp' to build project) **/
gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Sass', 'TypeScript'], callback);
});


gulp.task('bump', function(){
    gulp.src('./package.json')
        .pipe(bump({
            type: 'major',
            indent: 4
        }))
        .pipe(gulp.dest('./'));
});