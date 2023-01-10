window.initMap = function (){
    const map = new google.maps.Map(document.getElementById("map"),{
        center: { lat : 37.5400456, lng:126.9921017},
        zoom : 10,
    });
};