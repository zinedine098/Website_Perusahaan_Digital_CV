// Custom JavaScript for KursusKu

document.addEventListener('DOMContentLoaded', function() {
    // Fungsi untuk menangani penandaan pelajaran sebagai selesai
    const markCompleteButtons = document.querySelectorAll('.mark-complete-btn');
    
    markCompleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const lessonId = this.dataset.lessonId;
            const courseId = this.dataset.courseId;
            
            // Kirim permintaan ke server untuk menandai pelajaran sebagai selesai
            fetch(`/learning/mark-lesson-complete/${lessonId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    'lesson_id': lessonId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Perbarui tampilan tombol
                    this.innerHTML = '<i class="fas fa-check"></i> Sudah Selesai';
                    this.disabled = true;
                    this.classList.remove('btn-primary');
                    this.classList.add('btn-success');
                    
                    // Tampilkan pesan sukses
                    alert(data.message || 'Pelajaran berhasil ditandai sebagai selesai!');
                    
                    // Perbarui progress bar jika ada
                    updateProgressBar();
                } else {
                    alert(data.message || 'Gagal menandai pelajaran sebagai selesai.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat menandai pelajaran sebagai selesai.');
            });
        });
    });
    
    // Fungsi untuk memperbarui progress bar
    function updateProgressBar() {
        // Di sini Anda bisa menambahkan logika untuk memperbarui progress bar secara real-time
        // Bergantung pada implementasi backend Anda
    }
    
    // Fungsi untuk menangani rating pada form ulasan
    const ratingInputs = document.querySelectorAll('.rating-input input[type="radio"]');
    
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Hapus kelas aktif dari semua bintang
            const allStars = this.closest('.rating-input').querySelectorAll('.btn');
            allStars.forEach(star => star.classList.remove('btn-warning', 'btn-outline-warning'));
            
            // Tambahkan kelas aktif ke bintang yang dipilih dan sebelumnya
            const selectedValue = parseInt(this.value);
            for (let i = 1; i <= selectedValue; i++) {
                const star = this.closest('.rating-input').querySelector(`input[value="${i}"]`).closest('.btn');
                star.classList.add('btn-warning');
                star.classList.remove('btn-outline-warning');
            }
        });
    });
    
    // Inisialisasi semua rating yang sudah dipilih
    document.querySelectorAll('.rating-input').forEach(container => {
        const selectedInput = container.querySelector('input[type="radio"]:checked');
        if (selectedInput) {
            const selectedValue = parseInt(selectedInput.value);
            for (let i = 1; i <= selectedValue; i++) {
                const star = container.querySelector(`input[value="${i}"]`).closest('.btn');
                star.classList.add('btn-warning');
                star.classList.remove('btn-outline-warning');
            }
        }
    });
});

// Utility function untuk format angka
function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}