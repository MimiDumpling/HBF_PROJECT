
var questionVote = document.getElementById('question-vote');
var answerVote = document.getElementById('answer-vote');

function addQuestionVote() {
//figure out which question was up voted
    var question_span = document.getElementById('question_id'); debugger;
    var question_id = question_span.dataset.questionId;
    $.post("/question_vote/" + question_id,
            votingDone);
}

function votingDone(data) {
    alert(data);
}

questionVote.addEventListener('click', addQuestionVote);
