document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('viewer');
    console.log(container);
    if (!container) {
        console.error('URL du PDF non trouvée');
        return;
    } else {
        const url = container.getAttribute('data-url');
        console.log('URL du PDF : ' + url);
        // Chargez le document PDF
        pdfjsLib.getDocument(url).promise.then(function(pdf) {
            console.log('PDF chargé');
    
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                // Créez un élément canvas pour chaque page
                let canvas = document.createElement('canvas');
                canvas.id = 'page-' + pageNum;
                container.appendChild(canvas);
    
                // Chargez la page
                pdf.getPage(pageNum).then(function(page) {
                    console.log('Page ' + pageNum + ' chargée');
                    
                    const viewport = page.getViewport({scale: 1});
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
    
                    // Rendu de la page dans le canvas
                    const renderContext = {
                        canvasContext: canvas.getContext('2d'),
                        viewport: viewport
                    };
                    page.render(renderContext).promise.then(function() {
                        console.log('Page ' + pageNum + ' rendue');
                    });
                });
            }
        }, function(reason) {
            console.error(reason);
        });
    }
});
