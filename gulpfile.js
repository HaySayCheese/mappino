var gulp        = require('gulp'),
    del         = require('del'),
    rename      = require("gulp-rename"),

    runSequence = require('run-sequence'),

    sass        = require('gulp-sass'),
    minifyCSS   = require('gulp-minify-css'),

    typescript  = require('gulp-typescript'),

    imagemin    = require('gulp-imagemin'),
    pngquant    = require('imagemin-pngquant'),

    uglify      = require('gulp-uglify'),
    sourcemaps  = require('gulp-sourcemaps');



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



gulp.task('Clean', function(callback) {
    del([PATHS.BUILD.PATH + '*'], callback());
});





gulp.task('Copy:Fonts', function() {
    gulp.src(PATHS.SOURCE.FONTS + '/**/*.{ttf,woff,woff2,eot,svg}')
        .pipe(gulp.dest(PATHS.BUILD.FONTS));
});

gulp.task('Copy:Images', function() {
    gulp.src(PATHS.SOURCE.IMAGES + '/**/*.{png,jpg,jpeg,gif,svg}')
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{ removeViewBox: false }],
            use: [pngquant()]
        }))
        .pipe(gulp.dest(PATHS.BUILD.IMAGES));
});

gulp.task('Copy:Libraries', function() {
    gulp.src(PATHS.SOURCE.LIBRARIES + '/**/*.{js,ts}')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(PATHS.BUILD.LIBRARIES));
});

gulp.task('Copy', [
    'Copy:Fonts',
    'Copy:Images',
    'Copy:Libraries'
]);







gulp.task('Sass:Landing', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/landing/landing.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/landing/'));
});


gulp.task('Sass:Help', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/help/help.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/help/'));
});


gulp.task('Sass:Map', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/map/map.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/map/'));
});

gulp.task('Sass:Cabinet:Users', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/users/cabinet.users.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/users/'));
});

gulp.task('Sass:Cabinet:Moderators', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/moderators/cabinet.moderators.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/moderators/'));
});

gulp.task('Sass:Cabinet:Managers', function () {
    return gulp.src(PATHS.SOURCE.STYLES + '/cabinet/managers/cabinet.managers.scss')
        .pipe(sass())
        .pipe(minifyCSS())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(PATHS.BUILD.STYLES + '/cabinet/managers/'));
});

gulp.task('Sass', [
    'Sass:Landing',
    'Sass:Help',
    'Sass:Map',
    'Sass:Cabinet:Users',
    'Sass:Cabinet:Moderators',
    'Sass:Cabinet:Managers'
]);







gulp.task('TypeScript:Landing', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/landing/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'landing.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('/'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/landing/'));
});

gulp.task('TypeScript:Help', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/help/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'help.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('/'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/help/'));
});

gulp.task('TypeScript:Map', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/map/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'map.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/map/'));
});

gulp.task('TypeScript:Cabinet:Users', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/users/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'cabinet.users.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/users/'));
});

gulp.task('TypeScript:Cabinet:Moderators', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/moderators/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'cabinet.moderators.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/moderators/'));
});


gulp.task('TypeScript:Cabinet:Managers', function() {
    return gulp.src(PATHS.SOURCE.SCRIPTS + '/cabinet/managers/_all.ts')
        .pipe(sourcemaps.init())
        .pipe(typescript({
            noImplicitAny: false,
            target: 'ES5',
            out: 'cabinet.managers.js'
        }))
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(PATHS.BUILD.SCRIPTS + '/cabinet/managers/'));
});

gulp.task('TypeScript', [
    'TypeScript:Landing',
    'TypeScript:Help',
    'TypeScript:Map',
    'TypeScript:Cabinet:Users',
    'TypeScript:Cabinet:Moderators',
    'TypeScript:Cabinet:Managers'
]);






gulp.task('watch', function () {
    gulp.watch(PATHS.SOURCE.STYLES + '/common/**/*.scss',                 ['Sass']);
    gulp.watch(PATHS.SOURCE.STYLES + '/map/**/*.scss',                  ['Sass:Map']);
    gulp.watch(PATHS.SOURCE.STYLES + '/landing/**/*.scss',              ['Sass:Landing']);
    gulp.watch(PATHS.SOURCE.STYLES + '/help/**/*.scss',                 ['Sass:Help']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/users/**/*.scss',        ['Sass:Cabinet:Users']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/moderators/**/*.scss',   ['Sass:Cabinet:Moderators']);
    gulp.watch(PATHS.SOURCE.STYLES + '/cabinet/managers/**/*.scss',     ['Sass:Cabinet:Managers']);


    gulp.watch(PATHS.SOURCE.SCRIPTS + '/core/**/*.ts',                  ['TypeScript']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/map/**/*.ts',                   ['TypeScript:Map']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/landing/**/*.ts',               ['TypeScript:Landing']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/help/**/*.ts',                  ['TypeScript:Help']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/users/**/*.ts',         ['TypeScript:Cabinet:Users']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/moderators/**/*.ts',    ['TypeScript:Cabinet:Moderators']);
    gulp.watch(PATHS.SOURCE.SCRIPTS + '/cabinet/managers/**/*.ts',      ['TypeScript:Cabinet:Managers']);
});





gulp.task('default', function(callback) {
    runSequence('Clean', ['Copy', 'Sass', 'TypeScript'], callback);
});