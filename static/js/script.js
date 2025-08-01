// initialize once
document.addEventListener('DOMContentLoaded', () => {
  tinymce.init({
    selector: '#editor',
    width: '100%',
    height: window.innerHeight,
    plugins: [
      'advlist', 'autolink', 'link', 'charmap', 'media', 'preview',
      'pagebreak', 'searchreplace', 'wordcount', 'visualblocks', 
      'code', 'fullscreen', 'insertdatetime', 'table', 
      'emotions', 'codesample'
    ],
    toolbar: [
      'undo redo | styles | fontselect fontsizeselect | bold italic underline | ' +
      'alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | ' +
      'link image | forecolor backcolor | preview fullscreen'
    ],
    fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
    menubar: 'favs file edit view insert format table',
    content_style: 'body { font-family: Helvetica, Arial, sans-serif; font-size: 14px; }'
  });
});


function load_admin_lesson(id, title, content, parent_id) {
 
  document.getElementById('title').value = title;
  document.getElementById('parent_id').value = parent_id;
  
  
  tinymce.get('editor').setContent(content || '');
}
