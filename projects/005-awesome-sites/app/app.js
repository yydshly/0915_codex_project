const buttons = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.case')];
buttons.forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  cards.forEach(card => { card.hidden = filter !== '全部' && card.dataset.group !== filter; });
  document.querySelector('#result-status').textContent = `显示 ${cards.filter(card => !card.hidden).length} / ${cards.length} 个案例 · ${filter}`;
}));
document.querySelectorAll('.preview img').forEach(img => img.addEventListener('error', () => {
  img.hidden = true;
  const message = document.createElement('p');
  message.className = 'asset-error';
  message.textContent = '预览图暂不可用，点击访问原作。';
  img.parentElement.append(message);
}));
