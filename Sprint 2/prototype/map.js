function initMap() {
    const montreal = { lat: 45.508888, lng: -73.561668 }; // Montreal coordinates
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12, // Adjust the zoom level as needed
      center: montreal,
    });
  
    // You can add markers, polygons, or other features to the map as desired.
    // Example:
    const marker = new google.maps.Marker({
      position: montreal,
      map: map,
      title: "Montreal",
    });
  }
  