
var questionVote = document.getElementById('question-vote');
var answerVote = document.getElementById('answer-vote');

function addQuestionVote() {
//figure out which question was up voted
    var question_span = document.getElementById('question_id');
    var question_id = question_span.dataset.questionId;
    console.log(question_span);
    console.log(question_id);
    $.post("/question_vote/" + question_id + ".json", votingDone);
}

function votingDone(data) {
    alert(data);
    console.log("Hooray!");
    $('.question-vote-btn').attr("disabled", "disabled");
}

questionVote.addEventListener('click', addQuestionVote);
