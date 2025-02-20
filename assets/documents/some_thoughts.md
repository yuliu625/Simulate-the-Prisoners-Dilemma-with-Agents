# 一些想法

## Agent System
构建multi-agent system的目的在于，这样的系统会比single agent效果更好。对于具体的设定，复杂程度也可以有很多。

### system message prompt
通过初始的system message，可以赋予具体agent不同的设定。这点尤其在经过很好sft的模型上表现得更好。

### specific model client
可以选择不同的模型作为每个agent的base model。例如，多模态任务可以选择具有不同感知的模型。例如，可以选择具体阶段任务的专家模型，包括一般的LLM与SLM。

### context
这是我这个时候认为最重要的一点，模型接收和返回相关的信息。这里的理解是：如果退化为一般情况，一直保持全部的context会使得multi-agent system退化为类似CoT的prompt-based方法。更加灵活的对于context的设定，可以增强生成效果。因此，我对于multi-agent的通讯机制很重视。

### recursive agent system
这是进一步的相关思考。如果单个agent可以设计得很复杂，同时信息控制也可以做到，那么，可以单个agent系统内部是合作关系，外部之间是进行博弈。


## Experiment Config
由于闭源的更大参数规模的模型有更好的能力，本次初步的实验是prompt-based方法。

### model client
参与实验的agent应该是一样的，除了他们在实验中得到的信息。

具体的LLM应该选择推理能力和数学能力强的。

## Prompt Design
prompt的设计会很重要。

### System Prompt


