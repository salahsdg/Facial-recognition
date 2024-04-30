function deleteImage(imageId) {
  fetch("/delete-image", {
    method: "POST",
    body: JSON.stringify({ imageId: imageId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
