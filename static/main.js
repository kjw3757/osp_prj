function updateFileName(input) {
    var fileName = input.files[0].name; // 파일명 가져오기
        var uploadName = document.querySelector('.upload-name');
        uploadName.value = fileName; // 파일명을 .upload-name에 출력
    }