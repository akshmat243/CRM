// const notificationSocket = new WebSocket(
//     'ws://' + window.location.host + '/ws/notifications/'
// );

const notificationSocket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');




notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    alert(data.message);
    // const message = data['message'];

    // Show browser notification
    if (Notification.permission === 'granted') {
        
        new Notification('New Inquiry', { body: message });
    }
};

notificationSocket.onclose = function(e) {
    console.error('WebSocket closed unexpectedly');
};

// Request notification permission
if (Notification.permission !== 'granted') {
    
    Notification.requestPermission();
}