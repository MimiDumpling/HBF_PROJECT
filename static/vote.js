
var questionVote = document.getElementById('question-vote');
var answerVote = document.getElementById('answer-vote');

function addQuestionVote() {
    var question_span = document.getElementById('question_id');
    var question_id = question_span.dataset.questionId;
    console.log(question_span);
    console.log(question_id);
    $.post("/question_vote/" + question_id + ".json", questionVotingDone);
}

function questionVotingDone(data) {
    console.log("Hooray!");
    $('.question-vote-btn').attr("disabled");
    $('.question-vote-count').html(data);
}



questionVote.addEventListener('click', addQuestionVote);

