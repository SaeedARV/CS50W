document.addEventListener('DOMContentLoaded', function () {
    let editTag = document.querySelectorAll('.edit');

    editTag.forEach(ed => {
        ed.onclick = (event) => {

            const post = event.target.parentElement.parentElement;
            post.style.display = 'none';
            
            const text = post.children[1].innerHTML;

            const edit = post.nextElementSibling;
            edit.style.display = 'block';

            edit.innerHTML = `
            <form action="/editPost/${parseInt(post.dataset.post_id)}" method="post">
                <textarea name="textarea">${text}</textarea>
                <input type="submit">
            </form>
            `;

            const submit = edit.children[0].children[1];
            submit.addEventListener('click', function() {
                edit.children[0].children[0].innerHTML = edit.children[0].children[0].value;
                edit.style.display = 'none';

                post.children[1].innerHTML = edit.children[0].children[0].innerHTML;
                post.children[3].innerHTML = "edited";

                post.style.display = 'block';
            })
        }
    })
});
