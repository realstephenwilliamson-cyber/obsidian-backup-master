---
type: book-chapter
work: "[[Catalog/Philosophy/Lessig - Code Version 2.0]]"
book: "[[Library/Philosophy/Code Version 2.0 (Lessig)/Code Version 2.0 (Lessig)|Code Version 2.0 (Lessig)]]"
order: 7
source_pdf: "Library/Philosophy/Lessig - Code Version 2.0 (2006).pdf"
page_range: "38–60"
pdf_pages: "53–75"
text_source: "the PDF's own text layer (PyMuPDF)"
converted: 2026-10-22
---

[[Code v2 06 - Chapter 3. Is-Ism Is the Way It Is the Way It Must Be|← previous]] · [[Code Version 2.0 (Lessig)|contents]] · [[Code v2 08 - Chapter 5. Regulating Code|next →]]

*[p. 38]* ^pg53


## Chapter 4. Architectures of Control

THE INVISIBLE MAN DOESN’T FEAR THE STATE. HE KNOWS HIS NATURE PUTS HIM beyond its reach (unless he gets stupid, and of course, he always gets stupid). His story is the key to a general lesson: If you can’t know who someone is, or where he is, or what he’s doing, you can’t regulate him. His behavior is as he wants it to be. There’s little the state can do to change it.

So too with the original Internet: Everyone was an invisible man. As cyberspace was originally architected, there was no simple way to know who someone was, where he was, or what he was doing. As the Internet was originally architected, then, there was no simple way to regulate behavior there.

The aim of the last chapter, however, was to add a small but important point to this obvious idea: Whatever cyberspace was, there’s no reason it has to stay this way. The “nature” of the Internet is not God’s will. Its nature is simply the product of its design. That design could be different. The Net could be designed to reveal who someone is, where they are, and what they’re doing. And if it were so designed, then the Net could become, as I will argue throughout this part, the most regulable space that man has ever known.

In this chapter, I describe the changes that could—and are—pushing the Net from the unregulable space it was, to the perfectly regulable space it could be. These changes are not being architected by government. They are instead being demanded by users and deployed by commerce. They are not the product of some *1984*-inspired conspiracy; they are the consequence of changes made for purely pragmatic, commercial ends.

This obviously doesn’t make these changes bad or good. My purpose just now is not normative, but descriptive. We should understand where we are going, and why, before we ask whether this is where, or who, we want to be.

*[p. 39]* ^pg54

{TXB2} The history of the future of the Internet was written in Germany in January 1995. German law regulated porn. In Bavaria, it regulated porn heavily. CompuServe made (a moderate amount of, through USENET,) porn available to its users. CompuServe was serving Bavaria’s citizens. Bavaria told CompuServe to remove the porn from its servers, or its executives would be punished.

CompuServe at first objected that there was nothing it could do—save removing the porn from every server, everywhere in the world. That didn’t trouble the Germans much, but it did trouble CompuServe. So in January 1995, CompuServe announced a technical fix: Rather than blocking access to the USENET newsgroups that the Bavarians had complained about for all members of CompuServe, CompuServe had devised a technology to filter content on a country-by-country basis.<sup>1</sup>

To make that fix work, CompuServe had to begin to reckon who a user was, what they were doing, and where they were doing it. Technology could give them access to the data that needed reckoning. And with that shift, the future was set. An obvious response to a problem of regulability would begin to repeat itself.

CompuServe, of course, was not the Internet. But its response suggests the pattern that the Internet will follow. In this Chapter, I map just how the Internet can effectively be made to run (in this respect at least) like CompuServe.

WHO DID WHAT, WHERE?

To regulate, the state needs a way to know the who, in “Who did what, where?” To see how the Net will show the state “who,” we need to think a bit more carefully about how “identification” works in general, and how it might work on the Internet.

Identity and Authentication: Real Space

To make sense of the technologies we use to identify who someone is, consider the relationship among three familiar ideas—(1) “identity,” (2) “authentication,” and (3) “credential.”

By “identity” I mean something more than just who you are. I mean as well your “attributes,” or more broadly, all the facts about you (or a corporation, or a thing) that are true. Your identity, in this sense, includes your name, your sex, where you live, what your education is, your driver’s license number, your social security number, your purchases on Amazon.com, whether you’re a lawyer—and so on.

*[p. 40]* ^pg55

These attributes are known by others when they are communicated. In real space, some are communicated automatically: for most, sex, skin color, height, age range, and whether you have a good smile get transmitted automatically. Other attributes can’t be known unless they are revealed either by you, or by someone else: your GPA in high school, your favorite color, your social security number, your last purchase on Amazon, whether you’ve passed a bar exam.

Just because an attribute has been asserted, however, does not mean the attribute is believed. (“You passed the bar?!”) Rather belief will often depend upon a process of “authentication.” In general, we “authenticate” when we want to become more confident about the truth about some asserted claim than appears on its face. “I’m married,” you say. “Show me the ring,” she says. The first statement is an assertion about an attribute you claim you have. The second is a demand for authentication. We could imagine (in a comedy at least) that demand continuing. “Oh come on, that’s not a wedding ring. Show me your marriage license.” At some point, the demands stop, either when enough confidence has been achieved, or when the inquiry has just become too weird.

Sometimes this process of authentication is relatively automatic. Some attributes, that is, are relatively self-authenticating: You say you’re a woman; I’m likely to believe it when I see you. You say you’re a native speaker; I’m likely to believe it once I speak with you. Of course, in both cases, I could be fooled. Thus, if my life depended upon it, I might take other steps to be absolutely confident of what otherwise appears plain. But for most purposes, with most familiar sorts of attributes, we learn how to evaluate without much more than our own individual judgment.

Some attributes, however, cannot be self-authenticating. You say you’re licensed to fly an airplane; I want to see the license. You say you’re a member of the California bar; I want to see your certificate. You say you’re qualified to perform open heart surgery on my father; I want to see things that make me confident that your claim is true. Once again, these authenticating “things” could be forged, and my confidence could be unjustified. But if I’m careful to match the process for authentication with the level of confidence that I need, I’m behaving quite rationally. And most of us can usually get by without a terribly complicated process of authentication.

One important tool sometimes used in this process of authentication is a credential. By “credential,” I mean a standardized device for authenticating (to some level of confidence) an assertion made. A driver’s license is a credential in this sense. Its purpose is to authenticate the status of a driver. We’re generally familiar with the form of such licenses; that gives us some confidence

*[p. 41]* ^pg56

that we’ll be able to determine whether a particular license is valid. A passport is also a credential in this sense. Its purpose is to establish the citizenship of the person it identifies, and it identifies a person through relatively self-authenticating attributes. Once again, we are familiar with the form of this credential, and that gives us a relatively high level of confidence about the facts asserted in that passport.

Obviously, some credentials are better than others. Some are architected to give more confidence than others; some are more efficient at delivering their confidence than others. But we select among the credentials available depending upon the level of confidence that we need.

So take an obvious example to bring these points together: Imagine you’re a bank teller. Someone appears in front of you and declares that she is the owner of account # 654–543231. She says she would like to withdraw all the money from that account.

In the sense I’ve described, this someone (call her Ms. X) has asserted a fact about her identity—that she is the owner of account # 654–543231. Your job now is to authenticate that assertion. So you pull up on your computer the records for the account, and you discover that there’s lots of money in it. Now your desire to be confident about the authentication you make is even stronger. You ask Ms. X her name; that name matches the name on the account. That gives you some confidence. You ask Ms. X for two forms of identification. Both match to Ms. X. Now you have even more confidence. You ask Ms. X to sign a withdrawal slip. The signatures seem to match; more confidence still. Finally, you note in the record that the account was established by your manager. You ask her whether she knows Ms. X. She confirms that she does, and that the “Ms. X” standing at the counter is indeed Ms. X. Now you’re sufficiently confident to turn over the money.

Notice that throughout this process, you’ve used technologies to help you authenticate the attribute asserted by Ms. X to be true. Your computer links a name to an account number. A driver’s license or passport ties a picture to a name. The computer keeps a copy of a signature. These are all technologies to increase confidence.

And notice too that we could imagine even better technologies to increase this confidence. Credit cards, for example, were developed at a time when merely possessing the credit card authenticated its use. That design creates the incentive to steal a credit card. ATM cards are different—in addition to possession, ATM cards require a password. That design reduces the value of stolen cards. But some write their passwords on their ATM cards, or keep them in their wallets with their ATMs. This means the risk from theft is not totally removed. But that risk could be further reduced by other technologies

*[p. 42]* ^pg57

of authentication. For example, certain biometric technologies, such as thumbprint readers or eye scans, would increase the confidence that the holder of a card was an authorized user. (Though these technologies themselves can create their own risks: At a conference I heard a vendor describing a new technology for identifying someone based upon his handprint; a participant in the conference asked whether the hand had to be alive for the authentication to work. The vendor went very pale. After a moment, he replied, “I guess not.”)

We are constantly negotiating these processes of authentication in real life, and in this process, better technologies and better credentials enable more distant authentication. In a small town, in a quieter time, credentials were not necessary. You were known by your face, and your face carried with it a reference (held in the common knowledge of the community) about your character. But as life becomes more fluid, social institutions depend upon other technologies to build confidence around important identity assertions. Credentials thus become an unavoidable tool for securing such authentication.

If technologies of authentication can be better or worse, then, obviously, many have an interest in these technologies becoming better. We each would be better off if we could more easily and confidently authenticate certain facts about us. Commerce, too, would certainly be better off with better technologies of authentication. Poor technologies begat fraud; fraud is an unproductive cost for business. If better technology could eliminate that cost, then prices could be lower and profits possibly higher.

And finally, governments benefit from better technologies of authentication. If it is simple to authenticate your age, then rules that are triggered based upon age are more easily enforced (drinking ages, or limits on cigarettes). And if it is simple to authenticate who you are, then it will be easier for the government to trace who did what.

Fundamentally, the regulability of life in real-space depends upon certain architectures of authentication. The fact that witnesses can identify who committed a crime, either because they know the person or because of self-authenticating features such as “he was a white male, six feet tall,” enhances the ability of the state to regulate against that crime. If criminals were invisible or witnesses had no memory, crime would increase. The fact that fingerprints are hard to change and are now automatically traced to convicted felons increases the likelihood that felons will be caught again. Relying on a more changeable physical characteristic would reduce the ability of the police to track repeat offenders. The fact that cars have license plates and are registered by their owners increases the likelihood that a hit-and-run driver will be

*[p. 43]* ^pg58

caught. Without licenses, and without systems registering owners, it would be extremely difficult to track car-related crime. In all these cases, and in many more, technologies of authentication of real-space life make regulating that life possible.

These three separate interests therefore point to a common interest. That’s not to say that every technology of authentication meets that common interest, nor is it to say that these interests will be enough to facilitate more efficient authentication. But it does mean that we can see which way these interests push. Better authentication can benefit everyone.

Identity and Authentication: Cyberspace

Identity and authentication in cyberspace and real space are in theory the same. In practice they are quite different. To see that difference, however, we need to see more about the technical detail of how the Net is built.

As I’ve already said, the Internet is built from a suite of protocols referred to collectively as “TCP/IP.” At its core, the TCP/IP suite includes protocols for exchanging packets of data between two machines “on” the Net.<sup>2</sup> Brutally simplified, the system takes a bunch of data (a file, for example), chops it up into packets, and slaps on the address to which the packet is to be sent and the address from which it is sent. The addresses are called Internet Protocol addresses, and they look like this: 128.34.35.204. Once properly addressed, the packets are then sent across the Internet to their intended destination. Machines along the way (“routers”) look at the address to which the packet is sent, and depending upon an (increasingly complicated) algorithm, the machines decide to which machine the packet should be sent next. A packet could make many “hops” between its start and its end. But as the network becomes faster and more robust, those many hops seem almost instantaneous.

*[p. 44]* ^pg59

In the terms I’ve described, there are many attributes that might be associated with any packet of data sent across the network. For example, the packet might come from an e-mail written by Al Gore. That means the e-mail is written by a former vice president of the United States, by a man knowledgeable about global warming, by a man over the age of 50, by a tall man, by an American citizen, by a former member of the United States Senate, and so on. Imagine also that the e-mail was written while Al Gore was in Germany, and that it is about negotiations for climate control. The identity of that packet of information might be said to include all these attributes.

But the e-mail itself authenticates none of these facts. The e-mail may say it’s from Al Gore, but the TCP/IP protocol alone gives us no way to be sure. It may have been written while Gore was in Germany, but he could have sent it through a server in Washington. And of course, while the system eventually will figure out that the packet is part of an e-mail, the information traveling across TCP/IP itself does not contain anything that would indicate what the content was. The protocol thus doesn’t authenticate who sent the packet, where they sent it from, and what the packet is. All it purports to assert is an IP address to which the packet is to be sent, and an IP address from which the packet comes. From the perspective of the network, this other information is unnecessary surplus. Like a daydreaming postal worker, the network simply moves the data and leaves its interpretation to the applications at either end.

This minimalism in the Internet’s design was not an accident. It reflects a decision about how best to design a network to perform a wide range over very different functions. Rather than build into this network a complex set of functionality thought to be needed by every single application, this network philosophy pushes complexity to the edge of the network—to the applications that run on the network, rather than the network’s core. The core is kept as simple as possible. Thus if authentication about who is using the network is necessary, that functionality should be performed by an application connected to the network, not by the network itself. Or if content needs to be encrypted, that functionality should be performed by an application connected to the network, not by the network itself.

This design principle was named by network architects Jerome Saltzer, David Clark, and David Reed as the end-to-end principle.<sup>3</sup> It has been a core principle of the Internet’s architecture, and, in my view, one of the most important reasons that the Internet produced the innovation and growth that it has enjoyed. But its consequences for purposes of identification and authentication make both extremely difficult with the basic protocols of the Internet alone. It is as if you were in a carnival funhouse with the lights dimmed to darkness and voices coming from around you, but from people you do not

*[p. 45]* ^pg60

know and from places you cannot identify. The system knows that there are entities out there interacting with it, but it knows nothing about who those entities are. While in real space—and here is the important point—anonymity has to be created, in cyberspace anonymity is the given.

Identity and Authentication: Regulability

This difference in the architectures of real space and cyberspace makes a big difference in the regulability of behavior in each. The absence of relatively self-authenticating facts in cyberspace makes it extremely difficult to regulate behavior there. If we could all walk around as “The Invisible Man” in real space, the same would be true about real space as well. That we’re not capable of becoming invisible in real space (or at least not easily) is an important reason that regulation can work.

Thus, for example, if a state wants to control children’s access to “indecent” speech on the Internet, the original Internet architecture provides little help. The state can say to websites, “don’t let kids see porn.” But the website operators can’t know—from the data provided by the TCP/IP protocols at least—whether the entity accessing its web page is a kid or an adult. That’s different, again, from real space. If a kid walks into a porn shop wearing a mustache and stilts, his effort to conceal is likely to fail. The attribute “being a kid” is asserted in real space, even if efforts to conceal it are possible. But in cyberspace, there’s no need to conceal, because the facts you might want to conceal about your identity (i.e., that you’re a kid) are not asserted anyway.

All this is true, at least, under the basic Internet architecture. But as the last ten years have made clear, none of this is true by necessity. To the extent that the lack of efficient technologies for authenticating facts about individuals makes it harder to regulate behavior, there are architectures that could be layered onto the TCP/IP protocol to create efficient authentication. We’re far enough into the history of the Internet to see what these technologies could look like. We’re far enough into this history to see that the trend toward this authentication is unstoppable. The only question is whether we will build into this system of authentication the kinds of protections for privacy and autonomy that are needed.

Architectures of Identification

Most who use the Internet have no real sense about whether their behavior is monitored, or traceable. Instead, the experience of the Net suggests anonymity. Wikipedia doesn’t say “Welcome Back, Larry” when I surf to its

*[p. 46]* ^pg61

site to look up an entry, and neither does Google. Most, I expect, take this lack of acknowledgement to mean that no one is noticing.

But appearances are quite deceiving. In fact, as the Internet has matured, the technologies for linking behavior with an identity have increased dramatically. You can still take steps to assure anonymity on the Net, and many depend upon that ability to do good (human rights workers in Burma) or evil (coordinating terrorist plots). But to achieve that anonymity takes effort. For most of us, our use of the Internet has been made at least traceable in ways most of us would never even consider possible.

Consider first the traceability resulting from the basic protocols of the Internet—TCP/IP. Whenever you make a request to view a page on the Web, the web server needs to know where to sent the packets of data that will appear as a web page in your browser. Your computer thus tells the web server where you are—in IP space at least—by revealing an IP address.

As I’ve already described, the IP address itself doesn’t reveal anything about who you are, or where in physical space you come from. But it does enable a certain kind of trace. If (1) you have gotten access to the web through an Internet Service Provider (ISP) that assigns you an IP address while you’re on the Internet and (2) that ISP keeps the logs of that assignment, then it’s perfectly possible to trace your surfing back to you.

How?

Well, imagine you’re angry at your boss. You think she’s a blowhard who is driving the company into bankruptcy. After months of frustration, you decide to go public. Not “public” as in a press conference, but public as in a posting to an online forum within which your company is being discussed.

You know you’d get in lots of trouble if your criticism were tied back to you. So you take steps to be “anonymous” on the forum. Maybe you create an account in the forum under a fictitious name, and that fictitious name makes you feel safe. Your boss may see the nasty post, but even if she succeeds in getting the forum host to reveal what you said when you signed up, all that stuff was bogus. Your secret, you believe, is safe.

Wrong. In addition to the identification that your username might, or might not, provide, if the forum is on the web, then it knows the IP address from which you made your post. With that IP address, and the time you made your post, using “a reverse DNS look-up,”<sup>4</sup> it is simple to identify the Internet Service Provider that gave you access to the Internet. And increasingly, it is relatively simple for the Internet Service Provider to check its records to reveal which account was using that IP address at that specified time. Thus, the ISP could (if required) say that it was your account that was using the IP address that posted the nasty message about your boss. Try as you will to deny it

*[p. 47]* ^pg62

(“Hey, on the Internet, no one knows you’re a dog!”), I’d advise you to give up quickly. They’ve got you. You’ve been trapped by the Net. Dog or no, you’re definitely in the doghouse.

Now again, what made this tracing possible? No plan by the NSA. No strategy of Microsoft. Instead, what made this tracing possible was a by-product of the architecture of the Web and the architecture of ISPs charging access to the Web. The Web must know an IP address; ISPs require identification before they assign an IP address to a customer. So long as the log records of the ISP are kept, the transaction is traceable. Bottom line: If you want anonymity, use a pay phone!

This traceability in the Internet raised some important concerns at the beginning of 2006. Google announced it would fight a demand by the government to produce one million sample searches. (MSN and Yahoo! had both complied with the same request.) That request was made as part of an investigation the government was conducting to support its defense of a statute designed to block kids from porn. And though the request promised the data would be used for no other purpose, it raised deep concerns in the Internet community. Depending upon the data that Google kept, the request showed in principle that it was possible to trace legally troubling searches back to individual IP addresses (and to individuals with Google accounts). Thus, for example, if your Internet address at work is a fixed-IP address, then every search you’ve ever made from work is at least possibly kept by Google. Does that make you concerned? And assume for the moment you are not a terrorist: Would you still be concerned?

A link back to an IP address, however, only facilitates tracing, and again, even then not perfect traceability. ISPs don’t keep data for long (ordinarily); some don’t even keep assignment records at all. And if you’ve accessed the Internet at an Internet café, then there’s no reason to believe anything could be traced back to you. So still, the Internet provides at least some anonymity.

But IP tracing isn’t the only technology of identification that has been layered onto the Internet. A much more pervasive technology was developed early in the history of the Web to make the web more valuable to commerce and its customers. This is the technology referred to as “cookies.”

When the World Wide Web was first deployed, the protocol simply enabled people to view content that had been marked up in a special programming language. This language (HTML) made it easy to link to other pages, and it made it simple to apply basic formatting to the content (bold, or italics, for example).

But the one thing the protocol didn’t enable was a simple way for a website to know which machines had accessed it. The protocol was “state-less.”

*[p. 48]* ^pg63

When a web server received a request to serve a web page, it didn’t know anything about the state of the requester before that request was made.<sup>5</sup>

From the perspective of privacy, this sounds like a great feature for the Web. Why should a website know anything about me if I go to that site to view certain content? You don’t have to be a criminal to appreciate the value in anonymous browsing. Imagine libraries kept records of every time you opened a book at the library, even for just a second.

Yet from the perspective of commerce, this “feature” of the original Web is plainly a bug, and not because commercial sites necessarily want to know everything there is to know about you. Instead, the problem is much more pragmatic. Say you go to Amazon.com and indicate you want to buy 20 copies of my latest book. (Try it. It’s fun.) Now your “shopping cart” has 20 copies of my book. You then click on the icon to check out, and you notice your shopping cart is empty. Why? Well because, as originally architected, the Web had no easy way to recognize that you were the same entity that just ordered 20 books. Or put differently, the web server would simply forget you. The Web as originally built had no way to remember you from one page to another. And thus, the Web as originally built would not be of much use to commerce.

But as I’ve said again and again, the way the Web was is not the way the Web had to be. And so those who were building the infrastructure of the Web quickly began to think through how the web could be “improved” to make it easy for commerce to happen. “Cookies” were the solution. In 1994, Netscape introduced a protocol to make it possible for a web server to deposit a small bit of data on your computer when you accessed that server. That small bit of data—the “cookie”—made it possible for the server to recognize you when you traveled to a different page. Of course, there are lots of other concerns about what that cookie might enable. We’ll get to those in the chapter about privacy. The point that’s important here, however, is not the dangers this technology creates. The point is the potential and how that potential was built. A small change in the protocol for client-server interaction now makes it possible for websites to monitor and track those who use the site.

This is a small step toward authenticated identity. It’s far from that, but it is a step toward it. Your computer isn’t you (yet). But cookies make it possible for the computer to authenticate that it is the same machine that was accessing a website a moment before. And it is upon this technology that the whole of web commerce initially was built. Servers could now “know” that this machine is the same machine that was here before. And from that knowledge, they could build a great deal of value.

Now again, strictly speaking, cookies are nothing more than a tracing technology. They make it simple to trace a machine across web pages. That

*[p. 49]* ^pg64

tracing doesn’t necessarily reveal any information about the user. Just as we could follow a trail of cookie crumbs in real space to an empty room, a web server could follow a trail of “mouse droppings” from the first entry on the site until the user leaves. In both cases, nothing is necessarily revealed about the user.

But sometimes something important is revealed about the user by association with data stored elsewhere. For example, imagine you enter a site, and it asks you to reveal your name, your telephone number, and your e-mail address as a condition of entering a contest. You trust the website, and do that, and then you leave the website. The next day, you come back, and you browse through a number of pages on that website. In this interaction, of course, you’ve revealed nothing. But if a cookie was deposited on your machine through your browser (and you have not taken steps to remove it), then when you return to the site, the website again “knows” all these facts about you. The cookie traces your machine, and this trace links back to a place where you provided information the machine would not otherwise know.

The traceability of IP addresses and cookies is the default on the Internet now. Again, steps can be taken to avoid this traceability, but the vast majority of us don’t take them. Fortunately, for society and for most of us, what we do on the Net doesn’t really concern anyone. But if it did concern someone, it wouldn’t be hard to track us down. We are a people who leave our “mouse droppings” everywhere.

This default traceability, however, is not enough for some. They require something more. That was Harvard’s view, as I noted in the previous chapter. That is also the view of just about all private networks today. A variety of technologies have developed that enable stronger authentication by those who use the Net. I will describe two of these technologies in this section. But it is the second of these two that will, in my view, prove to be the most important.

The first of these technologies is the Single Sign-on (SSO) technology. This technology allows someone to “sign-on” to a network once, and then get access to a wide range of resources on that network without needing to authenticate again. Think of it as a badge you wear at your place of work. Depending upon what the badge says (“visitor” or “researcher”) you get different access to different parts of the building. And like a badge at a place of work, you get the credential by giving up other data. You give the receptionist an ID; he gives you a badge; you wear that badge wherever you go while at the business.

The most commonly deployed SSO is a system called Kerberos. But there are many different SSOs out there—Microsoft’s Passport system is an

*[p. 50]* ^pg65

example—and there is a strong push to build federated SSOs for linking many different sites on the Internet. Thus, for example, in a federated system, I might authenticate myself to my university, but then I could move across any domain within the federation without authenticating again. The big advantage in this architecture is that I can authenticate to the institution I trust without spreading lots of data about myself to institutions I don’t trust.

SSOs have been very important in building identity into the Internet. But a second technology, I believe, will become the most important tool for identification in the next ten years. This is because this alternative respects important architectural features of the Internet, and because the demand for better technologies of identification will continue to be strong. Forget the hassle of typing your name and address at every site you want to buy something from. You only need to think about the extraordinary growth in identity theft to recognize there are many who would be eager to see something better come along.

To understand this second system, think first about how credentials work in real space.<sup>6</sup> You’ve got a wallet. In it is likely to be a driver’s license, some credit cards, a health insurance card, an ID for where you work, and, if you’re lucky, some money. Each of these cards can be used to authenticate some fact about you—again, with very different levels of confidence. The driver’s license has a picture and a list of physical characteristics. That’s enough for a wine store, but not enough for the NSA. The credit card has your signature. Vendors are supposed to use that data to authenticate that the person who signs the bill is the owner of the card. If the vendor becomes suspicious, she might demand that you show an ID as well.

Notice the critical features of this “wallet” architecture. First, these credentials are issued by different entities. Second, depending upon their technology, they offer different levels of confidence. Third, I’m free to use these credentials in ways never originally planned or intended by the issuer of the credential. The Department of Motor Vehicles never coordinated with Visa to enable driver’s licenses to be used to authenticate the holder of a credit card. But once the one was prevalent, the other could use it. And fourth, nothing requires that I show all my cards when I can use just one. That is, to show my driver’s license, I don’t also reveal my health insurance card. Or to use my Visa, I don’t also have to reveal my American Express card.

These same features are at the core of what may prove to be the most important addition to the effective architecture of the Internet since its birth. This is a project being led by Microsoft to essentially develop an Identity Metasystem—a new layer of the Internet, an Identity Layer, that would complement the existing network layers to add a new kind of functionality. This

*[p. 51]* ^pg66

Identity Layer is not Microsoft Passport, or some other Single Sign-On technology. Instead it is a protocol to enable a kind of virtual wallet of credentials, with all the same attributes of the credentials in your wallet—except better. This virtual wallet will not only be more reliable than the wallet in your pocket, it will also give you the ability to control more precisely what data about you is revealed to those who demand data about you.

For example, in real space, your wallet can easily be stolen. If it’s stolen, then there’s a period of time when it’s relatively easy for the thief to use the cards to buy stuff. In cyberspace, these wallets are not easily stolen. Indeed, if they’re architected well, it would be practically impossible to “steal” them. Remove the cards from their holder, and they become useless digital objects.

Or again, in real space, if you want to authenticate that you’re over 21 and therefore can buy a six-pack of beer, you show the clerk your driver’s license. With that, he authenticates your age. But with that bit of data, he also gets access to your name, your address, and in some states, your social security number. Those other bits of data are not necessary for him to know. In some contexts, depending on how creepy he is, these data are exactly the sort you don’t want him to know. But the inefficiencies of real-space technologies reveal these data. This loss of privacy is a cost of doing business.

The virtual wallet would be different. If you need to authenticate your age, the technology could authenticate that fact alone—indeed, it could authenticate simply that you’re over 21, or over 65, or under 18, without revealing anything more. Or if you need to authenticate your citizenship, that fact can be certified without revealing your name, or where you live, or your passport number. The technology is crafted to reveal just what you want it to reveal, without also revealing other stuff. (As one of the key architects for this metasystem, Kim Cameron, described it: “To me, that’s the center of the system.”<sup>7</sup>) And, most importantly, using the power of cryptography, the protocol makes it possible for the other side to be confident about the fact you reveal without requiring any more data.

The brilliance in this solution to the problems of identification is first that it mirrors the basic architecture of the Internet. There’s no central repository for data; there’s no network technology that everyone must adopt. There is instead a platform for building identity technologies that encourages competition among different privacy and security providers—TCP/IP for identity. Microsoft may be leading the project, but anyone can build for this protocol. Nothing ties the protocol to the Windows operating system. Or to any other specific vendor. As Cameron wisely puts it, “it can’t be owned by any one company or any one country . . . or just have the technology stamp of any one engineer.”<sup>8</sup>

*[p. 52]* ^pg67

The Identity Layer is infrastructure for the Internet. It gives value (and raises concerns) to many beyond Microsoft. But though Microsoft’s work is an important gift to the Internet, the Identity Layer is not altruism. “Microsoft’s strategy is based on web services,” Cameron described to me. “Web services are impossible without identity.”<sup>9</sup> There is important public value here, but private interest is driving the deployment of this public value.

The Identity Layer would benefit individuals, businesses, and the government, but each differently. Individuals could more easily protect themselves from identity theft;<sup>10</sup> if you get an e-mail from PayPal demanding you update your account, you’ll know whether the website is actually PayPal. Or if you want to protect yourself against spam, you could block all e-mail that doesn’t come from an authenticated server. In either case, the technology is increasing confidence about the Internet. And the harms that come from a lack of confidence—mainly fraud—would therefore be reduced.

Commerce too would benefit from this form of technology. It too benefits from the reduction of fraud. And it too would benefit from a more secure infrastructure for conducting online transactions.

And finally, the government would benefit from this infrastructure of trust. If there were a simple way to demand that people authenticate facts about themselves, it would be easier for the government to insist that they do so. If it were easier to have high confidence that the person on the website was who he said he was, then it would be cheaper to deliver certain information across the web.

But while individuals, commerce, and government would all benefit from this sort of technology, there is also something that each could lose.

Individuals right now can be effectively anonymous on the Net. A platform for authenticated identity would make anonymity much harder. We might imagine, for example, a norm developing to block access to a website by anyone not carrying a token that at least made it possible to trace back to the user—a kind of driver’s license for the Internet. That norm, plus this technology, would make anonymous speech extremely difficult.

Commerce could also lose something from this design. To the extent that there are simple ways to authenticate that I am the authorized user of this credit card, for example, it’s less necessary for websites to demand all sorts of data about me—my address, my telephone numbers, and in one case I recently encountered, my birthday. That fact could build a norm against revealing extraneous data. But that data may be valuable to business beyond simply confirming a charge.

And governments, too, may lose something from this architecture of identification. Just as commerce may lose the extra data that individuals need

*[p. 53]* ^pg68

to reveal to authenticate themselves, so too will the government lose that. It may feel that such data is necessary for some other purpose, but gathering it would become more difficult.

Each of these benefits and costs can be adjusted, depending upon how the technology is implemented. And as the resulting mix of privacy and security is the product of competition and an equilibrium between individuals and businesses, there’s no way up front to predict what it will be.

But for our purposes, the only important fact to notice is that this infrastructure could effectively answer the first question that regulability requires answering: *Who* did what where? With an infrastructure enabling cheap identification wherever you are, the frequency of unidentified activity falls dramatically.

{TXB2} This final example of an identification technology throws into relief an important fact about encryption technology. The Identity Layer depends upon cryptography. It thus demonstrates the sense in which cryptography is Janus-faced. As Stewart Baker and Paul Hurst put it, cryptography “surely is the best of technologies and the worst of technologies. It will stop crimes and it will create new crimes. It will undermine dictatorships, and it will drive them to new excesses. It will make us all anonymous, and it will track our every transaction.”<sup>11</sup>

Cryptography can be all these things, both good and bad, because encryption can serve two fundamentally different ends. In its “confidentiality” function it can be “used to keep communications secret.” In its “identification” function it can be “used to provide forgery-proof digital identities.”<sup>12</sup> It enables freedom from regulation (as it enhances confidentiality), but it can also enable more efficient regulation (as it enhances identification).<sup>13</sup>

Its traditional use is secrets. Encrypt a message, and only those with the proper key can open and read it. This type of encryption has been around as long as language itself. But until the mid-1970s it suffered from an important weakness: the same key that was used to encrypt a message was also used to decrypt it. So if you lost that key, all the messages hidden with that key were also rendered vulnerable. If a large number of messages were encrypted with the same key, losing the key compromised the whole archive of secrets protected by the key. This risk was significant. You always had to “transport” the key needed to unlock the message, and inherent in that transport was the risk that the key would be lost.

In the mid-1970s, however, a breakthrough in encryption technique was announced by two computer scientists, Whitfield Diffie and Martin Hellman.<sup>14</sup> Rather than relying on a single key, the Diffie-Hellman system used

*[p. 54]* ^pg69

two keys—one public, the other private. What is encrypted with one can be decrypted only with the other. Even with one key there is no way to infer the other.

This discovery was the clue to an architecture that could build an extraordinary range of confidence into any network, whether or not the physical network itself was secure.<sup>15</sup> And again, that confidence could both make me confident that my secrets won’t be revealed and make me confident that the person using my site just now is you. The technology therefore works to keep secrets, but it also makes it harder to keep secrets. It works to make stuff less regulable, and more regulable.

In the Internet’s first life, encryption technology was on the side of privacy. Its most common use was to keep information secret. But in the Internet’s next life, encryption technology’s most important role will be in making the Net more regulable. As an Identity Layer gets built into the Net, the easy ability to demand some form of identity as a condition to accessing the resources of the Net increases. As that ability increases, its prevalence will increase as well. Indeed, as Shawn Helms describes, the next generation of the Internet Protocol—IPv6—“marks each packet with an encryption ‘key’ that cannot be altered or forged, thus securely identifying the packet’s origin. This authentication function can identify every sender and receiver of information over the Internet, thus making it nearly impossible for people to remain anonymous on the Internet.”<sup>16</sup>

And even if not impossible, sufficiently difficult for the vast majority of us. Our packets will be marked. We—or something about us—will be known.

WHO DID WHAT, WHERE?

Regulability also depends upon knowing the “what” in “who did what, where?” But again, the Internet as originally designed didn’t help the regulator here either. If the Internet protocol simply cuts up data into packets and stamps an address on them, then nothing in the basic protocol would tell anyone looking at the packet what the packet was for.

For example, imagine you’re a telephone company providing broadband Internet access (DSL) across your telephone lines. Some smart innovator develops Voice-over-IP (VOIP)—an application that makes it possible to use the Internet to make telephone calls. You, the phone company, aren’t happy about that, because now people using your DSL service can make unmetered telephone calls. That freedom cuts into your profit.

Is there anything you can do about this? Relying upon just the Internet protocols, the answer is no. The “packets” of data that contain the simulated-telephone

*[p. 55]* ^pg70

calls look just like any packet of data. They don’t come labeled with VOIP or any other consistent moniker. Instead, packets are simply marked with addresses. They are not marked with explanations of what is going on with each.

But as my example is meant to suggest, we can easily understand why some would be very keen to understand what packets are flowing across their network, and not just for anti-competitive purposes. Network administrators trying to decide whether to add new capacity need to know what the existing capacity is being used for. Businesses keen to avoid their employees wasting time with sports or porn have a strong interest in knowing just what their employees are doing. Universities trying to avoid viruses or malware being installed on network computers need to know what kind of packets are flowing onto their network. In all these cases, there’s an obvious and valid *will* to identify what packets are flowing on the network. And as they say, where there’s a will, there’s a way.

The way follows the same technique described in the section above. Again, the TCP/IP protocol doesn’t include technology for identifying the content carried in TCP/IP packets. But it also doesn’t interfere with applications that might examine TCP/IP packets and report what those packets are about.

So, for example, consider a package produced by Ipanema Technologies. This technology enables a network owner to inspect the packets traveling on its network. As its webpage promises,

The Ipanema Systems “deep” layer 7 packet inspection automatically recognizes all critical business and recreational application flows running over the network. Real-time graphical interfaces as well as minute-by-minute reports are available to rapidly discover newly deployed applications.<sup>17</sup>

Using the data gathered by this technology, the system generates reports about the applications being used in the network, and who’s using them. These technologies make it possible to control network use, either to economize on bandwidth costs, or to block uses that the network owner doesn’t permit.

Another example of this kind of content control is a product called “iProtectYou.”<sup>18</sup> This product also scans packets on a network, but this control is implemented at the level of a particular machine. Parents load this software on a computer; the software then monitors all network traffic with that computer. As the company describes, the program can then “filter harmful websites and newsgroups; restrict Internet time to a predetermined schedule; decide which programs can have Internet access; limit the amount of data that

*[p. 56]* ^pg71

can be sent or received to/from your computer; block e-mails, online chats, instant messages and P2P connections containing inappropriate words; \[and produce\] detailed Internet activity logs.” Once again, this is an application that sits on top of the network and watches. It intervenes in network activity when it identifies the activity as the kind the administrator wants to control.

In addition to these technologies of control, programmers have developed a wide range of programs to monitor networks. Perhaps the dominant application in this context is called “nmap”—a program

for network exploration or security auditing . . . designed to rapidly scan large networks. . . . Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, what services (application name and version) those hosts are offering, what operating systems (and OS versions) they are running, what type of packet filters/firewalls are in use, and dozens of other characteristics.<sup>19</sup>

This software is “free software,” meaning the source code is available, and any modifications of the source code must be made available as well. These conditions essentially guarantee that the code necessary to engage in this monitoring will always be available.

Finally, coders have developed “packet filtering” technology, which, as one popular example describes, “is the selective passing or blocking of data packets as they pass through a network interface. . . . The most often used criteria are source and destination address, source and destination port, and protocol.” This again is a technology that’s monitoring “what” is carried within packets, and decides what’s allowed based upon what it finds.

In each of these cases, a layer of code complements the TCP/IP protocol, to give network administrators something TCP/IP alone would not—namely, knowledge about “what” is carried in the network packets. That knowledge increases the “regulability” of network use. If a company doesn’t want its employees using IM chat, then these technologies will enforce that rule—by blocking the packets containing IM chat. Or if a company wants to know which employees use sexually explicit speech in Internet communication, these technologies will reveal that as well. Again, there are plenty of perfectly respectable reasons why network administrators might want to exercise this regulatory authority—even if there are plenty of cases where such power would be an abuse. Because of this legitimate demand, software products like this are developed.

Now, of course, there are countermeasures that users can adopt to avoid just this sort of monitoring. A user who encrypts the data he sends across the network will avoid any filtering on the basis of key words. And there are plenty

*[p. 57]* ^pg72

of technologies designed to “anonymize” behavior on the Net, so administrators can’t easily know what an individual is doing on a network. But these countermeasures require a significant investment for a particular user to deploy—whether of time or money. The vast majority won’t bother, and the ability of network administrators to monitor content and use of the network will be preserved.

Thus, as with changes that increased the ability to identify “who” someone is who is using a network, here too, private interests provide a sufficient incentive to develop technologies that make it increasingly easy to say “what” someone is doing who is using a network. A gap in the knowledge provided by the plain vanilla Internet is thus plugged by these privately developed technologies.

WHO DID WHAT, WHERE?

Finally, as long as different jurisdictions impose different requirements, the third bit of data necessary to regulate efficiently is knowing where the target of regulation is. If France forbids the selling of Nazi paraphernalia, but the United States does not, then a website wanting to respect the laws of France must know something about where the person accessing the Internet is coming from.

But once again, the Internet protocols didn’t provide that data. And thus, it would be extremely difficult to regulate or zone access to content on the basis of geography.

The original Internet made such regulation extremely difficult. As originally deployed, as one court put it:

The Internet is wholly insensitive to geographic distinctions. In almost every case, users of the Internet neither know nor care about the physical location of the Internet resources they access. Internet protocols were designed to ignore rather than document geographic location; while computers on the network do have “addresses,” they are logical addresses on the network rather than geographic addresses in real space. The majority of Internet addresses contain no geographic clues and, even where an Internet address provides such a clue, it may be misleading.<sup>20</sup>

But once again, commerce has come to the rescue of regulability. There are obvious reasons why it would useful to be able to identify where someone is when they access some website. Some of those reasons have to do with regulation—again, blocking Nazi material from the French, or porn from kids in Kansas. We’ll consider these reasons more extensively later in this book. For now, however, the most interesting reasons are those tied purely to commerce.

*[p. 58]* ^pg73

And, again, these commercial reasons are sufficient to induce the development of this technology.

Once again, the gap in the data necessary to identify someone’s location is the product of the way IP addresses are assigned. IP addresses are virtual addresses; they don’t refer to a particular geographic place. They refer to a logical place on the network. Thus, two IP addresses in principle could be very close to each other in number, but very far from each other in geography. That’s not the way, for example, zip codes work. If your zip code is one digit from mine (e.g., 94115 vs. 94116), we’re practically neighbors.

But this gap in data is simply the gap in data about where someone is deducible from his IP address. That means, while there’s no simple way to deduce from 23.214.23.15 that someone is in California, it is certainly possible to gather the data necessary to map where someone is, given the IP address. To do this, one needs to construct a table of IP addresses and geographic locations, and then track both the ultimate IP address and the path along which a packet has traveled to where you are from where it was sent. Thus while the TCP/IP protocol can’t reveal where someone is directly, it can be used indirectly to reveal at least the origin or destination of an IP packet.

The commercial motivations for this knowledge are obvious. Jack Goldsmith and Tim Wu tell the story of a particularly famous entrepreneur, Cyril Houri, who was inspired to develop IP mapping technology. Sitting in his hotel in Paris one night, he accessed his e-mail account in the United States. His e-mail was hosted on a web server, but he noticed that the banner ads at the top of the website were advertising an American flower company. That gave him a (now obvious) idea: Why not build a tool to make it easy for a website to know from where it is being accessed, so it can serve relevant ads to those users?<sup>21</sup>

Houri’s idea has been copied by many. Geoselect, for example, is a company that provides IP mapping services. Just browse to their webpage, and they’re 99 percent likely to be able to tell you automatically where you are browsing from. Using their services, you can get a geographical report listing the location of the people who visit your site, and you can use their products to automatically update log files on your web server with geographic data. You can automatically change the greeting on your website depending upon where the user comes from, and you can automatically redirect a user based upon her location. All of this functionality is invisible to the user. All he sees is a web page constructed by tools that know something that the TCP/IP alone doesn’t reveal—where someone is from.

So what commercial reasons do websites have for using such software? One company, MaxMind,<sup>22</sup> lists the major reason as credit card fraud: If your

*[p. 59]* ^pg74

customer comes from a “high risk IP address”—meaning a location where it’s likely the person is engaged in credit card fraud—then MaxMind’s service will flag the transaction and direct that it have greater security verification. Max-Mind also promises the service will be valuable for “targeted advertising.” Using its product, a client can target a message based upon country, state, or city, as well as a “metropolitan code,” an area code, and connection speed of the user (no need to advertise DVD downloads to a person on a dial-up connection).

Here too there is an important and powerful open source application that provides the same IP mapping functions. Hostip.info gives website operators—for free—the ability to “geolocate” the users of their site.<sup>23</sup> This again means that the core functionality of IP mapping is not held exclusively by corporations or a few individuals. Any application developer—including a government—could incorporate the function into its applications. The knowledge and functionality is free.

Thus, again, one of the original gaps in the data necessary to make behavior regulable on the Internet—geographic identity—has been filled. But it has not been filled by government mandate or secret NSA operations (or so I hope). Instead, the gap has been filled by a commercial interest in providing the data the network itself didn’t. Technology now layers onto the Internet to produce the data the network needs.

But it is still possible to evade identification. Civil liberty activist Seth Finkelstein has testified to the relative ease with which one can evade this tracking.<sup>24</sup> Yet as I will describe more below, even easily evaded tracking can be effective tracking. And when tied to the architectures for identity described above, this sort will become quite effective.

RESULTS

In the last chapter, we saw that the unregulability of the Internet was a product of design: that the failure of that network to identify who someone is, what they’re doing, and where they’re from meant that it would be particularly difficult to enforce rules upon individuals using the network. Not impossible, but difficult. Not for all people, but for enough to matter. The Internet as it originally was gave everyone a “Ring of Gyges,” the ring which, as Plato reports in *The Republic,* made Gyges the shepherd invisible. The dilemma for regulation in such a world is precisely the fear Plato had about this ring: With such a ring, “no man can be imagined to be of such an iron nature that he would stand fast in justice.”<sup>25</sup>

And if such a man did choose justice, even with the power of the ring, then “he would be thought by the lookers-on to be a most wretched idiot,

*[p. 60]* ^pg75

although they would praise him to one another’s faces, and keep up appearances with one another from a fear that they too might suffer injustice.”

But these gaps in the Internet’s original design are not necessary. We can imagine networks that interact seamlessly with the Internet but which don’t have these “imperfections.” And, more importantly, we can see why there would be an important commercial interest in eliminating these gaps.

Yet you may still be skeptical. Even if most Internet activity is traceable using the technologies that I’ve described, you may still believe there are significant gaps. Indeed, the explosion of spam, viruses, ID theft, and the like are strong testimony to the fact that there’s still a lot of unregulable behavior. Commerce acting alone has not yet eliminated these threats, to both commerce and civil life. For reasons I explore later in this book, it’s not even clear commerce could.

But commerce is not the only actor here. Government is also an important ally, and the framework of regulability that commerce has built could be built on again by government.

Government can, in other words, help commerce and help itself. How it does so is the subject of the chapter that follows.
