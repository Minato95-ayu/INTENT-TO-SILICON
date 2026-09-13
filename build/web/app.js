const state = {};


function updateState(key, value) {
    state[key] = value;
    let bindEl = document.getElementById('bind_' + key);
    if (bindEl) {
        bindEl.innerText = value;
    }
}
