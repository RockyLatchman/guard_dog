

const accountModalHTML = `
      <div id="account-modal">
       <form method="post" action="/account-manager">
          <input type="text" name="name" placeholder="Name" required>
          <input type="email" name="email" placeholder="E-mail" required>
          <input type="password" name="password" placeholder="Password" required>
          <input type="tel" name="mobile" placeholder="Mobile" required>
          <input type="text" name="category" placeholder="Category" required>
          <label>Due date</label>
          <input type="date" name="due_date" required>
          <input type="text" name="amount" placeholder="Amount" required>
          <textarea name="note" placeholder="Note"></textarea>
          <input type="submit" value="Add account">
       </form>
      </div> `;

function createTemplate(templateHTML){
  const template = document.createElement('template');
  template.innerHTML = templateHTML;
  return template.content;
}

function createOverlay(){
  const overlay = document.createElement('div');
  overlay.setAttribute('class', 'overlay');
  return overlay;
}

function createModal(){
  const modalTemplate = createTemplate(accountModalHTML);
  const overlay = createOverlay();
  overlay.appendChild(modalTemplate);
  document.body.appendChild(overlay);
}

function addAccountItem(){
  if (location.pathname == '/account-manager') {
    const addAccountItem = document.querySelector('#add-item');
    addAccountItem.addEventListener('click', (e) => {
        e.preventDefault();
        createModal();
    });
  }
}

window.addEventListener('DOMContentLoaded', (e) => {
  addAccountItem();
});
