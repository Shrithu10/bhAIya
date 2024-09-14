window.addEventListener('beforeunload', (event) => {
    console.log('User is leaving the page');
    const data = JSON.stringify({"Status": "User is leaving the page"});
    navigator.sendBeacon('/save_chat_history', data);
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const imageUpload = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');
    const username = document.getElementById('username');
    const email = document.getElementById('user-email');
    const newChatButton = document.getElementById('new-chat-button');
    const chatHistoryList = document.getElementById('chat-history-list');

    const priceSlider = document.getElementById('priceSlider');
    const priceValue = document.getElementById('priceValue');
    const userInfo = document.getElementById('userInfo');
    const userMenu = document.getElementById('userMenu');

    const bundleButton = document.getElementById('bundle-button');

    bundleButton.addEventListener('click', async function generateBundles(event) {
    console.log('Generating bundles');
    
        addMessage('Generating personalized bundle recommendations...', 'received');

    // Show loading animation
    const typingIndicator = showTypingIndicator();
    
    try {
        const response = await fetch('/personal_recommendations', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        const data = await response.json();
        console.log(data);

        // Remove loading animation
        removeTypingIndicator(typingIndicator);

        // Render the data as HTML in a product grid
        let responseHTML = 'Here are some personalized bundle recommendations for you:';
        responseHTML += '<div class="product-grid">';
        
        data.forEach(item => {
            const [score, product] = item;
            responseHTML += `
                <div class="item">
                    <img src="data:image/jpeg;base64,${product.image}" alt="${product.id}">
                    <p>Price: $${product.price}</p>
                    <p>ID: ${product.id}</p>
                    <p>Category: ${product['Main category'].join(', ')}</p>
                    <a href="/item/${product.id}" class="view-product" data-id="${product.id}" data-price="${product.price}">View</a>
                    <button class="add-to-cart-btn" data-product-id="${product.id}" onclick="handleAddToCart(event)">Add to Cart</button>
                </div>
            `;
        });
        
        responseHTML += '</div>';

        // Add the message to the chat
        addMessage(responseHTML, 'received');
        saveChatToServer();

        // Add event listeners for the new buttons
        document.querySelectorAll('.view-product').forEach(btn => {
            btn.addEventListener('click', handleViewProduct);
        });
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', handleAddToCart);
        });
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingIndicator);
        addMessage('Sorry, there was an error generating bundle recommendations.', 'received');
        saveChatToServer();
    }
});
    
        // Price slider functionality
    priceSlider.addEventListener('input', function() {
        const value = this.value;
        priceValue.textContent = `₹${value}`;
        localStorage.setItem('priceRange', value);
    });

    // Load price range from local storage
    const savedPriceRange = localStorage.getItem('priceRange');
    if (savedPriceRange) {
        priceSlider.value = savedPriceRange;
        priceValue.textContent = `₹${savedPriceRange}`;
    }

    // User profile menu toggle
    userInfo.addEventListener('click', function() {
        userMenu.style.display = userMenu.style.display === 'flex' ? 'none' : 'flex';
    });

    // Close user menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!userInfo.contains(event.target) && !userMenu.contains(event.target)) {
            userMenu.style.display = 'none';
        }
    });

    // Load cart items
    function loadCartItems() {
        fetch('/get_cart_items')
            .then(response => response.json())
            .then(data => {
                console.log('Received cart items:', data);
                const cartPreview = document.getElementById('cartPreview');
                cartPreview.innerHTML = '';
                data.forEach(item => {
                    console.log(item);
                    updateCartPreview(item.id, `data:image/jpeg;base64,${item.image}`, item.count);
                });
            })
            .catch(error => console.error('Error loading cart items:', error));
    }

    // Call loadCartItems when the page loads
    loadCartItems();

    let conversations = {};
    let currentConversationId = null;

    function loadConversationsFromServer() {
        fetch('/get_chat_history')
            .then(response => response.json())
            .then(data => {
                conversations = data.conversations || {};
                currentConversationId = data.currentConversationId;
                updateConversationsList();
                loadCurrentConversation();
            })
            .catch(error => console.error('Error loading chat history:', error));
    }

    function createNewConversation() {
        const conversationId = Date.now().toString();
        conversations[conversationId] = [];
        saveChatToServer();
        return conversationId;
    }

    function switchConversation(conversationId) {
        saveChatToServer();
        currentConversationId = conversationId;
        loadCurrentConversation();
    }

    function loadCurrentConversation() {
        if (!currentConversationId || !conversations[currentConversationId]) {
            currentConversationId = createNewConversation();
        }
        chatMessages.innerHTML = '';
        conversations[currentConversationId].forEach(message => {
            addMessageToDOM(message.content, message.type, message.imageUrl);
        });
    }

    function updateConversationsList() {
        chatHistoryList.innerHTML = '';
        Object.keys(conversations).forEach((conversationId) => {
            const conversation = conversations[conversationId];
            if (conversation.length > 0) {
                const firstMessage = conversation.find(msg => msg.type === 'sent');
                if (firstMessage) {
                    const li = document.createElement('li');
                    li.className = 'conversation-item';
                    const date = new Date(parseInt(conversationId));
                    const formattedDate = date.toLocaleString('en-US', { 
                        month: 'short', 
                        day: 'numeric', 
                        year: 'numeric', 
                        hour: 'numeric', 
                        minute: 'numeric'
                    });
                    li.innerHTML = `
                        <div class="conversation-date">${formattedDate}</div>
                        <div class="conversation-preview">${firstMessage.content}</div>
                    `;
                    li.onclick = () => switchConversation(conversationId);
                    chatHistoryList.appendChild(li);
                }
            }
        });
    }

    function saveChatToServer() {
        const data = {
            conversations: conversations,
            currentConversationId: currentConversationId
        };

        fetch('/save_chat_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log('Chat history saved:', data))
        .catch(error => console.error('Error saving chat history:', error));
    }

    function fetchUserProfile() {
        fetch('/get_profile')
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data);
            username.textContent = data.username;
            if (conversations[currentConversationId].length === 0) {
                addMessage(`Hello, ${username.textContent}! I am bhAIya, your neighbourhood shopkeeper. How can I help?`, 'received');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function addMessage(content, type, imageUrl = null) {
        addMessageToDOM(content, type, imageUrl);
        if (currentConversationId) {
            conversations[currentConversationId].push({ content, type, imageUrl, timestamp: Date.now() });
            saveChatToServer();
        }
    }

    function addMessageToDOM(content, type, imageUrl = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        let messageContent;
        if(content){
            messageContent = `<p>${content}`;
        }
        if (imageUrl) {
            messageContent = `<img src="${imageUrl}" alt="User uploaded image"><p>${content}`;
        }
        if(messageContent){
            messageDiv.innerHTML = messageContent;
        }
        console.log(messageDiv)
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }

    function removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }

    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Image preview">
                    <span class="delete-image">&times;</span>
                `;
                imagePreview.querySelector('.delete-image').addEventListener('click', function() {
                    imagePreview.innerHTML = '';
                    imageUpload.value = '';
                });
            }
            reader.readAsDataURL(file);
        }
    });

    
const modeSwitch = document.getElementById('mode-switch');

// Add event listener for form submission
form.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    const userMessage = userInput.value.trim();
    const uploadedImage = imageUpload.files[0];

    if (userMessage || uploadedImage) {
        let imageUrl = null;
        if (uploadedImage) {
            imageUrl = URL.createObjectURL(uploadedImage);
        }
        addMessage(userMessage, 'sent', imageUrl);
        userInput.value = '';
        imagePreview.innerHTML = '';
        imageUpload.value = '';
        const typingIndicator = showTypingIndicator();

        // Check the state of the toggle switch
        if (!modeSwitch.checked) {
            // Toggle is off, use the original behavior
            fetch('/get_recommendations', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Received data:", data);
                removeTypingIndicator(typingIndicator);
                let responseHTML = 'Hey! Found something you might like. Take a look:';
                if (Array.isArray(data) && data.length > 0) {
                    responseHTML += '<div class="product-grid">';
                    console.log(data)
                    data.forEach(item => {
                        console.log(item);
                        let base64Image = item.image;
                        if (base64Image.startsWith("b'")) {
                            base64Image = base64Image.slice(2, -1);
                        }
                        responseHTML += `
                            <div class="item">
                                <img src="data:image/jpeg;base64,${base64Image}" alt="${item.id}">
                                <p>Price: ${item.price}</p>
                                <p>ID: ${item.id}</p>
                                <a href="/item/${item.id}" class="view-product" data-id="${item.id}" data-image="${base64Image}" data-price="${item.price}">View</a>
                                <button class="add-to-cart-btn" data-product-id="${item.id}" onclick="handleAddToCart(event)">Add to Cart</button>
                            </div>
                        `;
                    });
                    responseHTML += '</div>';
                } else {
                    responseHTML = 'Sorry, I couldn\'t find any recommendations.';
                }
                addMessage(responseHTML, 'received');
                saveChatToServer();
                document.querySelectorAll('.view-btn').forEach(btn => {
                    btn.addEventListener('click', handleViewProduct);
                });
                document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                    btn.addEventListener('click', handleAddToCart);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                removeTypingIndicator(typingIndicator);
                addMessage('Sorry, there was an error processing your request.', 'received');
                saveChatToServer();
            });
        } else {
            // Toggle is on, use the new behavior
            fetch('https://f84d-122-187-108-202.ngrok-free.app/custom_image_gen', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Received custom image data:", data);
                removeTypingIndicator(typingIndicator);
                let responseHTML = 'Here\'s a custom image based on your request:';
                
                // Assuming the API returns an object with a single key-value pair
                const [description, base64Image] = Object.entries(data)[0];
                
                responseHTML += `
                    <div class="custom-image-container">
                        <img src="data:image/jpeg;base64,${base64Image}" alt="${description}">
                        <button class="custom-product-btn">Custom Product</button>
                    </div>
                `;
                
                addMessage(responseHTML, 'received');
                saveChatToServer();
                
                // Add event listener for the Custom Product button if needed
                // document.querySelector('.custom-product-btn').addEventListener('click', handleCustomProduct);
            })
            .catch(error => {
                console.error('Error:', error);
                removeTypingIndicator(typingIndicator);
                addMessage('Sorry, there was an error generating a custom image.', 'received');
                saveChatToServer();
            });
        }
    }
});

    async function viewProduct(event) {
        if (event.target.classList.contains('view-product')) {
            event.preventDefault();
            const id = event.target.getAttribute('data-id');
            const image = event.target.getAttribute('data-image');
            const price = event.target.getAttribute('data-price');
    
            // Store the image and price in sessionStorage
            sessionStorage.setItem(`product_${id}_image`, image);
            sessionStorage.setItem(`product_${id}_price`, price);
    
            
            console.log('Viewing product:', id);
        try {
            const response = await fetch('/view-product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: id }),
            });
            const data = await response.json();
            if (data.success) {
                console.log('Product viewed successfully');
            }
        } catch (error) {
            console.error('Error viewing product:', error);
        }
        // Navigate to the product page
        window.location.href = `/item/${id}`;
        }
        
    }

   document.addEventListener('click', viewProduct);

    newChatButton.addEventListener('click', function() {
        saveChatToServer();
        switchConversation(createNewConversation());
        fetchUserProfile(); // This will add the initial greeting message
    });

    // Sidebar functionality
    const sideDrawer = document.getElementById('sideDrawer');
    const drawerHandle = document.getElementById('drawerHandle');
    let isDragging = false;
    let isHandleActive = false;
    let startX, startLeft;
    let longPressTimer;
    const longPressDuration = 300; // milliseconds
    
    // Initialize the drawer on the right side
    sideDrawer.classList.add('left');
    
    function openDrawer() {
        sideDrawer.classList.add('open');
        document.getElementById('chat-messages').classList.add('shifted_messages');
        document.querySelector('.chat-input').classList.add('shifted_input');
    }
    
    function closeDrawer() {
        sideDrawer.classList.remove('open');
        document.getElementById('chat-messages').classList.remove('shifted_messages');
        document.querySelector('.chat-input').classList.remove('shifted_input');
    }
    
    function toggleDrawer() {
        sideDrawer.classList.toggle('open');
        document.getElementById('chat-messages').classList.toggle('shifted_messages');
        document.querySelector('.chat-input').classList.toggle('shifted_input');
    }
    
    drawerHandle.addEventListener('mousedown', startLongPress);
    drawerHandle.addEventListener('touchstart', startLongPress);
    
    document.addEventListener('mousemove', drag);
    document.addEventListener('touchmove', drag);
    
    document.addEventListener('mouseup', endDrag);
    document.addEventListener('touchend', endDrag);
    
    // Toggle drawer when clicking the handle
    drawerHandle.addEventListener('click', () => {
        toggleDrawer();
    });
    
    function startLongPress(e) {
        e.preventDefault(); // Prevent default behavior
        isHandleActive = true; // Indicate that the handle was the initial target
        startX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        startLeft = sideDrawer.offsetLeft;
    
        longPressTimer = setTimeout(() => {
            isDragging = true;
            sideDrawer.classList.add('dragging');
        }, longPressDuration);
    }
    
    function drag(e) {
        if (!isDragging) return;
    
        const currentX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        const diffX = currentX - startX;
        const newLeft = startLeft + diffX;
    
        if (newLeft > window.innerWidth / 2) {
            sideDrawer.style.left = '';
            sideDrawer.style.right = '0';
            sideDrawer.classList.remove('left');
            sideDrawer.classList.add('right');
        } else {
            sideDrawer.style.right = '';
            sideDrawer.style.left = '0';
            sideDrawer.classList.remove('right');
            sideDrawer.classList.add('left');
        }
    
        openDrawer();
    }
    
    function endDrag(e) {
        clearTimeout(longPressTimer);
    
        if (isDragging) {
            isDragging = false;
            sideDrawer.classList.remove('dragging');
        }
    
        // Reset the handle active state
        isHandleActive = false;
    }

    // Initialize
    loadConversationsFromServer();
    fetchUserProfile();
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', handleViewProduct);
    });
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', handleAddToCart);
    });
});


async function handleAddToCart(e) {
    const productId = e.target.getAttribute('data-product-id');
    const productImage = e.target.closest('.item').querySelector('img').src;
    console.log('Adding product to cart:', productId);
    try {
        const response = await fetch('/add-to-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId }),
        });
        const data = await response.json();
        if (data.success) {
            console.log('Product added to cart successfully');
            updateCartPreview(productId, productImage);
        }
    } catch (error) {
        console.error('Error adding product to cart:', error);
    }

    
}

function updateCartPreview(productId, productImage, count = 1) {
    const cartPreview = document.getElementById('cartPreview');
    let itemElement = cartPreview.querySelector(`[data-product-id="${productId}"]`);
    
    if (itemElement) {
        // If the item is already in the preview, update the count
        const countElement = itemElement.querySelector('.item-count');
        const currentCount = parseInt(countElement.textContent, 10);
        countElement.textContent = currentCount + 1;
    } else {
        // If the item is not in the preview, add it
        itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.setAttribute('data-product-id', productId);
        itemElement.innerHTML = `
            <img src="${productImage}" alt="Product ${productId}">
            <span class="item-count">${count}</span>
        `;
        cartPreview.appendChild(itemElement);
    }
}


