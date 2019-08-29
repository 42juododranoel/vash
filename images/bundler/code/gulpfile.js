'use strict';
 
var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var minify = require('gulp-minify');
var cleanCSS = require('gulp-clean-css');

sass.compiler = require('node-sass');
 
gulp.task('compile-main-scss', function () {
  return gulp.src('styles/main/main.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('assets/styles'));
});

gulp.task('compile-other-scss', function () {
  return gulp.src('styles/other/*.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('assets/styles'));
});

gulp.task('compile-js', function() {
  return gulp.src('scripts/*.js')
    .pipe(minify({noSource: true, ext: {min: '.min.js'}}))
    .pipe(gulp.dest('assets/scripts'));
});

gulp.task('watch-compile', function () {
  gulp.watch('styles/main/*.scss', gulp.series('compile-main-scss'));
  gulp.watch('styles/other/*.scss', gulp.series('compile-other-scss'));
  gulp.watch('scripts/**/*.js', gulp.series('compile-js'));
});
