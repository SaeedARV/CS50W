document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#allPosts-button').addEventListener('click', () => load_allPosts());
    button = document.querySelector('#following-button');
    if(button){
         button.addEventListener('click', () => load_following());
    }

    load_allPosts()
    
});

function load_allPosts(){

    document.querySelector('#followingPosts-view').style.display = 'none';
    document.querySelector('#allPosts-view').style.display = 'block';

}
function load_following(){

    document.querySelector('#followingPosts-view').style.display = 'block';
    document.querySelector('#allPosts-view').style.display = 'none';

}
