document.addEventListener('DOMContentLoaded', function() {
    // Initialize drag and drop functionality for quick links
    initDragAndDrop();
});

function initDragAndDrop() {
    const grid = document.querySelector('.quick-links-grid');
    if (!grid) return;
    
    // Add drag and drop attributes to cards
    const cards = grid.querySelectorAll('.quick-link-card');
    cards.forEach((card, index) => {
        card.setAttribute('draggable', 'true');
        card.setAttribute('data-index', index);
        
        card.addEventListener('dragstart', handleDragStart);
        card.addEventListener('dragover', handleDragOver);
        card.addEventListener('dragenter', handleDragEnter);
        card.addEventListener('dragleave', handleDragLeave);
        card.addEventListener('drop', handleDrop);
        card.addEventListener('dragend', handleDragEnd);
    });
}

let dragSrcEl = null;

function handleDragStart(e) {
    dragSrcEl = this;
    
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
    
    this.classList.add('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    
    e.dataTransfer.dropEffect = 'move';
    
    return false;
}

function handleDragEnter(e) {
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    if (dragSrcEl !== this) {
        // Swap the cards
        const tempHTML = dragSrcEl.innerHTML;
        const tempBG = dragSrcEl.style.backgroundColor;
        
        dragSrcEl.innerHTML = this.innerHTML;
        dragSrcEl.style.backgroundColor = this.style.backgroundColor;
        
        this.innerHTML = tempHTML;
        this.style.backgroundColor = tempBG;
    }
    
    return false;
}

function handleDragEnd(e) {
    const cards = document.querySelectorAll('.quick-link-card');
    cards.forEach(card => {
        card.classList.remove('dragging');
        card.classList.remove('drag-over');
    });
}