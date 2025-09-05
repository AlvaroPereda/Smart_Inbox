document.addEventListener('DOMContentLoaded', function() {
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBarFill = document.getElementById('progress-bar-fill');

    function startProgressBar() {
        progressBarContainer.style.display = 'block';
        progressBarFill.style.width = '0%';
        let progress = 0;
        window.progressInterval = setInterval(() => {
            progress = Math.min(progress + Math.random() * 2, 90);
            progressBarFill.style.width = progress + '%';
        }, 800);
    }

    function stopProgressBar() {
        clearInterval(window.progressInterval);
        progressBarFill.style.width = '100%';
        setTimeout(() => {
            progressBarContainer.style.display = 'none';
            progressBarFill.style.width = '0%';
        }, 500);
    }

    document.getElementById('reload-btn').addEventListener('click', function() {
        document.getElementById('summary').innerHTML = '<p>Cargando resumen...</p>';
        startProgressBar();
        fetch('/api/chat')
            .then(response => response.json())
            .then(data => {
                stopProgressBar();
                const summaryDiv = document.getElementById('summary');
                summaryDiv.innerHTML = '';
                if (data.length === 0) {
                    summaryDiv.innerHTML = '<p>No hay correos para hoy.</p>';
                } else {
                    data.forEach((resumen) => {
                        const card = document.createElement('div');
                        card.className = 'email-summary-card';
                            // Detectar si es importante
                            let importante = false;
                            let asunto = 'Correo';
                            let contenido = resumen.response;
                            if (contenido.startsWith('IMPORTANTE')) {
                                importante = true;
                                contenido = contenido.replace(/^IMPORTANTE\s*/, '');
                            }
                            const asuntoMatch = contenido.match(/Asunto:\s*(.*)/);
                            if (asuntoMatch) {
                                asunto = asuntoMatch[1].trim();
                                contenido = contenido.replace(/Asunto:\s*.*\n?/, '');
                            }
                            contenido = contenido.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
                            contenido = contenido.replace(/\n/g, '<br>');
                            card.innerHTML = `${importante ? '<div class="important-banner">&#9888; IMPORTANTE</div>' : ''}<h3>${asunto}</h3><p>${contenido}</p>`;
                            if (importante) card.classList.add('important');
                            summaryDiv.appendChild(card);
                    });
                }
            })
            .catch(err => {
                stopProgressBar();
                document.getElementById('summary').innerHTML = '<p>Error al obtener el resumen.</p>';
            });
    });
});
