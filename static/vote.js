
var questionVote = document.getElementById('question-vote');
var answerVote = $('.answer-vote-btn');

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

function addAnswerVote(evt) {
    evt.preventDefault();
    // currentTarget is the specific button that was clicked
    var answer_button = $(evt.currentTarget);
    // .data() returns the value defined for the data attribute passed in
    var answer_id = answer_button.data("answer-id");
    console.log(answer_id);
    $.post("/answer_vote/" + answer_id + ".json", function(data) {
        console.log("Hooray!");
        answer_button.attr("disabled");
        // find all elements with answer-vote-count class, that also have
        // the data-answer-id attribute with the value answer_id
        $(".answer-vote-count[data-answer-id='" + answer_id + "']").html(data);
    });
}

// if answerVote is falsy (does it exist), the second part of && won't run
answerVote && answerVote.on('click', addAnswerVote);

// if questionVote is falsy (does it exist), the second part of && won't run
questionVote && questionVote.addEventListener('click', addQuestionVote);

