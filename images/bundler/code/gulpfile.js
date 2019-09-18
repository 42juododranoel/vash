'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var minify = require('gulp-minify');
var cleanCSS = require('gulp-clean-css');

sass.compiler = require('node-sass');

gulp.task('compile-scss', function () {
  return gulp.src(['resources/styles/*.scss', '!resources/styles/_*.scss'])
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('resources/assets/styles'));
});

gulp.task('compile-js', function() {
  return gulp.src(['resources/scripts/*.js', '!resources/scripts/_*.js'])
    .pipe(minify({noSource: true, ext: {min: '.min.js'}}))
    .pipe(gulp.dest('resources/assets/scripts'));
});

gulp.task('watch-compile', function () {
  gulp.watch(['resources/styles/*.scss'], gulp.series('compile-scss'));
  gulp.watch(['resources/scripts/*.js'], gulp.series('compile-js'));
});
