let currentNodeId = null;

tinymce.init({
  selector: '#editor',
  plugins: 'link image media lists',
  toolbar: 'undo redo | styleselect | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media',
  height: 400,
  setup: function (editor) {
    editor.on('init', function () {
      initTree(); // Load tree once TinyMCE is ready
    });
  }
});

// 🟩 Initialize tree using Fancytree
function initTree() {
  $("#tree").fancytree({
    source: { url: "/api/tree" },
    activate: function (event, data) {
      const node = data.node;
      currentNodeId = node.key;
      loadLesson(currentNodeId);
    }
  });
}

// 🟦 Load selected lesson content
async function loadLesson(id) {
  const res = await fetch(`/api/load/${id}`);
  const data = await res.json();
  document.getElementById("title").value = data.title;
  tinymce.get("editor").setContent(data.content);
}

// 🟨 Save title + content
async function save() {
  if (!currentNodeId) return alert("Select a lesson first.");
  const title = document.getElementById("title").value;
  const content = tinymce.get("editor").getContent();

  const res = await fetch(`/api/save/${currentNodeId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content })
  });

  if (res.ok) {
    alert("Saved!");
    reloadTree();
  } else {
    alert("Save failed.");
  }
}

// 🟩 Add a sublesson under the selected one
async function addSub() {
  if (!currentNodeId) return alert("Select a parent lesson.");
  const title = prompt("Enter sublesson title:");
  if (!title) return;

  const res = await fetch(`/api/add/${currentNodeId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });

  if (res.ok) {
    reloadTree();
  }
}

// 🟥 Delete current lesson
async function deleteLesson() {
  if (!currentNodeId) return alert("Select a lesson to delete.");
  if (!confirm("Are you sure? This will delete all sub-lessons too.")) return;

  const res = await fetch(`/api/delete/${currentNodeId}`, {
    method: "DELETE"
  });

  if (res.ok) {
    alert("Deleted.");
    currentNodeId = null;
    document.getElementById("title").value = "";
    tinymce.get("editor").setContent("");
    reloadTree();
  }
}

// ♻️ Refresh tree (e.g. after save/add/delete)
function reloadTree() {
  $("#tree").fancytree("getTree").reload();
}
