var data_file = document.currentScript.getAttribute('data_file');
$(document).ready(function(){

    var movies_div = `
    <div class="movies">
    `
    $.getJSON(data_file, function(json) {
        $.each(json, function(title, values){
            var movie_div = 
            `
            <div class="movie__container">
                <a href="https://www.imdb.com/title/tt${values.id}/" target="_blank" class="movie__item">
                    <img src="${values.image}" alt="${title}" class="portfolio__img">
                <div class="movie_overlay">
                    <div class="movie-text">
                        <p class="movie-title">${title}</p>
                    </div>
                </div>
                </a>
            </div>
            `
            movies_div = movies_div + movie_div
        });
        movies_div = movies_div + `
        </div>
        `
        $('#shows').append(movies_div)
    });

});