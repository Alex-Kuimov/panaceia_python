let tinyMce = {
    init: function(){
        tinymce.init({
          selector: '.article-form #id_text',
          plugins: [
            'advlist autolink lists link image charmap print preview anchor',
            'searchreplace visualblocks code fullscreen',
            'insertdatetime media table paste imagetools wordcount'
          ],
          toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
          content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
        });
    }
}

export { tinyMce }