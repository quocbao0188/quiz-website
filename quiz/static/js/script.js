//Get the button
var mybutton = document.getElementById("myBtn");
// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};
$(document).ready(function() {
  
})

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

$(".delete-btn").on('click', function() {
  var comment_id = $(this).attr('data-comment-id')
 
  $comment = $(this).closest('.post-comments')
  $('.delete-comment-modal').modal('show')
  $('.delete-comment-confirm').on('click', function(){
    $.ajax({
      url: '/comment/delete/',
      data: {
        comment_id: comment_id
      },
      dataType: "json",
      success: function(data) {
        $comment.hide()
        $('.delete-comment-modal').modal('hide')
      },
    })
  })
})

$('.comment-submit').on('click', function() {
  var comment_context = $(".comment-input").val()
  var document_id = $(".document-id").val()
  $comment = $(this).closest('.post-comments')
  var currentDate = moment().format('MMM D, YYYY, h:mm a');
  $.ajax({
    url: "/comment/create/",
    data: {
      content: comment_context,
      doc_id: document_id,
      user: loginUser
    },
    dataType: "json",
    success: function(data){
      $('.comment-container').append(
        '<div class="post-comments">' +
          '<div class="media">' +
              '<div class="media-body">' +
                  '<div class="media-heading">' +
                      '<h4>' + data["username"] + '</h4>' +
                      '<span class="time">' + currentDate + '</span>' +
                      '<a class="btn btn-danger btn-sm delete-btn" data-comment-id="2"><i class="fas fa-times"></i></a>' +
                  '</div>' +
                  '<p>' + data["content"] + '</p>' +
              '</div>' +
          '</div>' +
        '</div>'
        )
    }
  })

})