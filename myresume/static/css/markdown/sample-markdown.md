# Markdown 

You just have to love the simplicity of **markdown**, it doens't
provide a lot of fancy features that _reStructured Text_ or _Textile_
do, but in return, you get a wonderfully straightforward way to create
formatted documents, with almost zero overhead.

It seems to me that technical authors probably have the most to gain
from using **markdown**, this is probably why the most popular
technical sites on the web use it as their primary text markup
language.

## In Emacs Markdown is awesome.

#### Especially when you customize the faces...

    M-x customize-group
    markdown
    
And set some pleasant fonts for your headings, I like Helvetica Neue.

* * * * * 

Lists are phenomenally easy too ... 

1. Just number each item with 1.
1. The markdown implementation of your choice will turn it into a
numbered list.
1. Although, I think you will get varying levels of cleverness from
different implementations...
  1. Nested lists work ok. 
  1. But I find as soon as you start to get a bit clever, things tend to go
  wrong. You won't have much luck tring to use a combination of code
  blocks or blockquotes
  
  > See what I mean?
  > What did I tell you?
  
      (defn code-blocks (seriously)
          "it could work!!"
          )

  1. But then what about resuming the list, nah, I don't think so.
  
1. Still, it's much better than doing:

This....
     
    <ol> 
       <li>
    </ol>






