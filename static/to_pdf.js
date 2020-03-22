function Export(element_id, pdf_name) {
    html2canvas(document.getElementById(element_id), {
        onrendered: function (canvas) {
            var data = canvas.toDataURL();
            var docDefinition = {
                content: [{
                    image: data,
                    width: 500
                }]
            };
            pdfMake.createPdf(docDefinition).download(pdf_name);
        }
    });
}
