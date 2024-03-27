import gulp from 'gulp';
import gulpSass from 'gulp-sass';
import * as sass from 'sass';
import rename from 'gulp-rename';
import cssnano from 'gulp-cssnano';
import terser from 'gulp-terser';

const sassCompiler = gulpSass(sass);

function getPath(path) {
    const parts = path.basename.split('_');
    if (parts.length > 1) {
        path.dirname = parts[0] + '/static/' + (path.extname === '.js' || path.extname === '.mjs' ? 'js' : 'css');
        path.basename = parts.slice(1).join('_');
    } else {
        path.dirname = path.basename + '/static/' + (path.extname === '.js' || path.extname === '.mjs' ? 'js' : 'css');
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
  
// Compilation et minification JS et MJS
function compileJs() {
    return gulp.src(['js/**/*.js', 'js/**/*.mjs']) // Inclure les fichiers .js et .mjs
        .pipe(terser()) // Utiliser terser pour la minification
        .pipe(rename(path => {
            getPath(path);
            path.extname = '.min.js'; // Notez que l'extension .mjs est renommée en .js pour la sortie minifiée
        }))
        .pipe(gulp.dest('.'));
}

// Surveillance des modifications des fichiers SCSS
function watchScss() {
    gulp.watch('scss/**/*.scss', compileScss);
}

// Surveillance des modifications des fichiers JS
function watchJs() {
    gulp.watch(['js/**/*.js', 'js/**/*.mjs'], compileJs);
}

export default gulp.series(
    gulp.parallel(compileScss, compileJs),
    gulp.parallel(watchScss, watchJs)
);
