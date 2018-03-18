$.getJSON('vision_data.json', function (vision_data) {
    window.vision_data = vision_data;

    $(document).ready(function () {
        var emoji_angry = document.querySelector('img.emoji-angry');
        var emoji_joy = document.querySelector('img.emoji-joy');
        var emoji_neutral = document.querySelector('img.emoji-neutral');
        var emoji_sad = document.querySelector('img.emoji-sad');
        var emoji_surprised = document.querySelector('img.emoji-surprised');

        var img = document.querySelector('div#image > img');
        $(img).after('<canvas id="canvas" width="' + img.naturalWidth + '" height="' + img.naturalHeight + '"></canvas>');

        var canvas = document.querySelector('#canvas').getContext("2d");

        canvas.drawImage(img, 0, 0);

        for (var f = 0; f < vision_data.length; f++) {
            var face_data = vision_data[f];

            var left = Number.MAX_VALUE;
            var right = Number.MIN_VALUE;
            var top = Number.MIN_VALUE;
            var bottom = Number.MAX_VALUE;

            // var bounds = new Path2D();
            for (var v = 0; v < face_data.vertices.length; v++) {
                var x = face_data.vertices[v].x;
                var y = face_data.vertices[v].y;
                // if (v === 0) {
                //     bounds.moveTo(x, y);
                // } else {
                //     bounds.lineTo(x, y);
                // }

                if (x < left) left = x;
                if (x > right) right = x;
                if (y > top) top = y;
                if (y < bottom) bottom = y;
            }
            // bounds.lineTo(face_data.vertices[0].x, face_data.vertices[0].y);
            // canvas.stroke(bounds);

            var emoji;
            if (face_data.dominant_emotion === 'anger') {
                emoji = emoji_angry;
            } else if (face_data.dominant_emotion === 'joy') {
                emoji = emoji_joy;
            } else if (face_data.dominant_emotion === 'neutral') {
                emoji = emoji_neutral;
            } else if (face_data.dominant_emotion === 'sorrow') {
                emoji = emoji_sad;
            } else if (face_data.dominant_emotion === 'surprise') {
                emoji = emoji_surprised;
            }

            var w = right - left;
            var h = bottom - top;

            canvas.save();
            canvas.translate(left + (w / 2), top + (h / 2));
            canvas.rotate(face_data.roll * Math.PI / 180);
            canvas.drawImage(emoji, -w / 2, -h / 2, w, h);
            canvas.restore();
        }
    });
});
