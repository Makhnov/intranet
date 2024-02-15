import gulp from 'gulp';
import gulpSass from 'gulp-sass';
import * as sass from 'sass';
import rename from 'gulp-rename';
import uglify from 'gulp-uglify';
import cssnano from 'gulp-cssnano';

const sassCompiler = gulpSass(sass);

function getPath(path) {
    const parts = path.basename.split('_');
    if (parts.length > 1) {
      path.dirname = parts[0] + '/static/' + (path.extname === '.js' ? 'js' : 'css');
      path.basename = parts.slice(1).join('_');
    } else {
      path.dirname = path.basename + '/static/' + (path.extname === '.js' ? 'js' : 'css');
    }
}
  
// Compilation et minification SCSS
function compileScss() {
    return gulp.src('scss/**/*.scss')
        .pipe(sassCompiler().on('error', sassCompiler.logError))
        .pipe(cssnano({
            reduceIdents: false, // Désactive la réduction des identifiants
            discardComments: {
                removeAll: true // Supprime tous les commentaires
            },
            discardUnused: false // Désactive la suppression des règles non utilisées
        }))
        .pipe(rename(path => {
            getPath(path);
            path.extname = '.min.css';  // Ajout de '.min' au nom du fichier
        }))
        .pipe(gulp.dest('.'));
}
  
// Compilation et minification JS
function compileJs() {
    return gulp.src('js/**/*.js')
        .pipe(uglify())  // Minification JS
        .pipe(rename(path => {
            getPath(path);
            path.extname = '.min.js';  // Ajout de '.min' au nom du fichier
        }))
        .pipe(gulp.dest('.'));
}

// Surveillance des modifications des fichiers SCSS
function watchScss() {
  gulp.watch('scss/**/*.scss', compileScss);
}

// Surveillance des modifications des fichiers JS
function watchJs() {
  gulp.watch('js/**/*.js', compileJs);
}

export default gulp.series(
  gulp.parallel(compileScss, compileJs),
  gulp.parallel(watchScss, watchJs)
);
