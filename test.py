function addAnswerVote() {
    var answer_span = document.getElementById('answer_id');
    var question_id = answer_span.dataset.answerId;
    console.log(answer_span);
    console.log(answer_id);
    $.post("/answer_vote/" + question_id + ".json", answerVotingDone);
}

function answerVotingDone(data) {
    console.log("Hooray!");
    $('.answer-vote-btn').attr("disabled");
    $('.answer-vote-count').html(data);
}

answerVote.addEventListener('click', addAnswerVote);



<p>
              Current Votes:
              <span class="answer-vote-count">{{ answer.answer_votes | length }}</span>
            </p>

              <button {% if answer.user.user_id in answer.answer_votes %} disabled {% endif %}
                      id="answer-vote"
                      class="answer-vote-btn" 
                      data-default-text="Vote This Answer Up!"
                      data-alt-text="Thanks for Voting">
                <span class="icon"></span> 
                <span class="text">Vote This Question Up!</span>
              </button>



@app.route("/answer_vote/<question_id>.json", methods=['POST'])
def calculates_answer_vote(question_id):
    """Calculates number of votes a answer has accrued."""

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    answer = Answer.query.get(question_id)
    answer_voting = answer.answer_votes
    answer_vote_count = len(answer.answer_votes)

    if AnswerVotes.query.filter(AnswerVotes.answer_id == answer_id, 
                                    AnswerVotes.user_id == user_id).first():

        flash("You've already voted for this question.")

    else:
        new_answer_vote = AnswerVotes(user_id=user_id,
                                        question_id=question_id,
                                        answer_id=answer_id)
        answer_vote_count += 1
        db.session.add(new_answer_vote)
        db.session.commit()

    return jsonify(answer_vote_count)
