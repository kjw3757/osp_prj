
document.addEventListener("DOMContentLoaded", function () {
    const sectionBtns = document.querySelectorAll(".faq-section h3.section-btn");

    // 질문 섹션 버튼 클릭 시 하위 질문들을 토글하는 이벤트 처리
    sectionBtns.forEach(function (sectionBtn) {
        sectionBtn.addEventListener("click", function () {
            const targetId = this.dataset.target;
            const targetContent = document.getElementById(targetId);

            // 다른 섹션의 버튼 비활성화
            sectionBtns.forEach(function (btn) {
                btn.classList.remove("active");
            });

            // 클릭한 섹션의 버튼 활성화
            this.classList.add("active");

            // 하위 질문들 토글
            targetContent.classList.toggle("show");
        });
    });
});