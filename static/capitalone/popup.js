urls = {
    app_content_url: "http://52.77.240.18:8081/app_content"
}

$(document).ready(function(){
    $(".transactions").click(function(){
        $(this).addClass("selected");
        $(".subscriptions").removeClass("selected");
		$(".details-subscription").removeClass("visible");
		$(".details-subscription").addClass("invisible");
		$(".details-transaction").removeClass("invisible");
		$(".details-transaction").addClass("visible");
    });
    $(".subscriptions").click(function(){
        $(this).addClass("selected");
        $(".transactions").removeClass("selected");
		$(".details-transaction").removeClass("visible");
		$(".details-transaction").addClass("invisible");
		$(".details-subscription").removeClass("invisible");
		$(".details-subscription").addClass("visible");
    });

    $.getJSON(urls.app_content_url, function(data) {
        addValToDiv('.balance .current .amount', data.curr_bal.val);
        addValToDiv('.balance .current .text-sub', data.curr_bal.val);

        addValToDiv('.balance .available .amount', data.credit.val);
        addValToDiv('.balance .available .text-sub', data.credit.val);

        addTransactionsToList('.transactions_list', data.transactions, '');
        addTransactionsToList('.details-subscription ul', data.subscriptions, 'scheduled');
    })
});

function addValToDiv(identifier, val) {
    $(identifier).html(val);
}

function addTransactionsToList(identifier, transactions, additional_class) {
    template_li = $('.template_trans_li');

    $.each(transactions, function(index, transaction) {
        console.log(transaction)
        $(identifier).append('<li>' + 
            '<div class="name">' + transaction.name + '</div>' +
            '<div class="timestamp">' + transaction.date + '</div>' +
            '<div class="amount ' + (transaction.amount[0] == '-' ? 'negative' : '') + additional_class + '">' + transaction.amount + '</div>' +
            '</li>')
    })
}