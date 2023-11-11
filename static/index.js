const creat_project_link = document.getElementById('creat-project-link');
const creat_project = document.getElementById('creat-project');
const listproject = document.getElementById('listproject');
const projectLink = document.getElementById('project-link');
const reportLink = document.getElementById('gozaresh');
const project_Content = document.getElementById('sub-sabt');
const reportContent = document.getElementById('sub-gozaresh');
const edit_btn = document.getElementById('edit-btn');
const delete_project_link = document.getElementById('delete-project-link');
const delete_project = document.getElementById('delete-project');
const edit_project = document.getElementById('edit-project');
const editProjectLink = document.getElementById('edit-project-link');
const editProjectDiv = document.getElementById('edit-project');
const search_by_name_link = document.getElementById('search-by-name-link');
const search_by_name = document.getElementById('search-by-name');
const search_by_start_link = document.getElementById('search-by-start-link')
const search_by_start = document.getElementById('search-by-start');
const search_by_end_link = document.getElementById('search-by-end-link')
const search_by_end = document.getElementById('search-by-end');
const search_by_mount_link = document.getElementById('search-by-mount-link')
const search_by_mount = document.getElementById('search-by-mount');
const search_financial = document.getElementById('search-financial');
const financial_Link = document.getElementById('financial-link');


function removeandmake (element) {
    element.style.display = 'block';
    const siblings = element.parentNode.children;
    for (let sibling of siblings) {
    if (sibling !== element) {
        sibling.style.display = 'none';
    }
    }
}

function closser(){
    project_Content.classList.remove('active');
    reportContent.classList.remove('active');
}


projectLink.addEventListener('click', () => {
if (project_Content.classList.contains('active')) {
    project_Content.classList.remove('active');
    reportContent.classList.remove('active');
} else {
    project_Content.classList.add('active');
    reportContent.classList.remove('active');
}
});

reportLink.addEventListener('click', () => {
    if (reportContent.classList.contains('active')) {
        reportContent.classList.remove('active');
        project_Content.classList.remove('active');
    } else {
        reportContent.classList.add('active');
        project_Content.classList.remove('active');
    }
});



editProjectLink.addEventListener('click', () =>{
    removeandmake(editProjectDiv);
    closser();
});

creat_project_link.addEventListener('click', () =>{
    removeandmake(creat_project);
    closser();
});

delete_project_link.addEventListener('click', () =>{
    removeandmake(delete_project);
    closser();
});

search_by_name_link.addEventListener('click', () =>{
    removeandmake(search_by_name);
    closser();
});

search_by_start_link.addEventListener('click', () =>{
    removeandmake(search_by_start);
    closser();
});

search_by_end_link.addEventListener('click', () =>{
    removeandmake(search_by_end);
    closser();
});

search_by_mount_link.addEventListener('click', () =>{
    removeandmake(search_by_mount);
    closser();
});
financial_Link.addEventListener('click', () =>{
    removeandmake(search_financial);
    closser();
});

ClassicEditor
.create(document.querySelector('#editor'))
.then(editor => {
    console.log('ویرایشگر متن آماده است.');
    const fontSizeSelector = document.querySelector('#fontSize');
    fontSizeSelector.addEventListener('change', (event) => {
        const fontSize = event.target.value;
        editor.execute('fontSize', { value: fontSize });
    });
})
.catch(error => {
    console.error(error);
});