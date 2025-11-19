#!/usr/bin/env python3
"""
Clean LLM Tool Calling Test
No hardcoded queries - only keyboard input for testing LLM tool selection
"""

import asyncio
import json
import sys
import os

# Add the tools directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from tools import get_client, convert_retail_tools_to_openai
from retail_tools import EcommerceTools


def get_executors():
    """Get all available tool executors"""
    return {
        "cancel_order": EcommerceTools.cancel_order,
        "search_products": EcommerceTools.search_products,
        "return_order": EcommerceTools.return_order,
        "place_order": EcommerceTools.place_order,
        "track_order": EcommerceTools.track_order,
        "update_address": EcommerceTools.update_address,
        "add_to_cart": EcommerceTools.add_to_cart,
        "remove_from_cart": EcommerceTools.remove_from_cart,
        "update_payment_method": EcommerceTools.update_payment_method,
        "apply_discount_code": EcommerceTools.apply_discount_code,
        "get_order_history": EcommerceTools.get_order_history,
        "schedule_delivery": EcommerceTools.schedule_delivery,
        "update_profile": EcommerceTools.update_profile,
        "contact_support": EcommerceTools.contact_support
    }


async def execute_tool_calls(tool_calls, executors):
    """Execute all tool calls and return results"""
    results = []
    
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"\n  🔧 Calling: {tool_name}")
        print(f"  📝 Args: {json.dumps(arguments, ensure_ascii=False)}")
        
        executor = executors.get(tool_name)
        if executor:
            try:
                result = executor(**arguments)
                print(f"  ✅ Success: {json.dumps(result, ensure_ascii=False)}")
                results.append({
                    "tool_call_id": tool_call.id,
                    "result": result,
                    "success": True
                })
            except Exception as e:
                print(f"  ❌ Error: {e}")
                results.append({
                    "tool_call_id": tool_call.id,
                    "result": {"error": str(e)},
                    "success": False
                })
        else:
            print(f"  ⚠️  Tool not found: {tool_name}")
            results.append({
                "tool_call_id": tool_call.id,
                "result": {"error": f"Tool {tool_name} not found"},
                "success": False
            })
    
    return results


async def chat_loop():
    """Main chat loop for testing LLM tool calling"""
    print("\n" + "="*70)
    print("🧪 LLM TOOL CALLING TEST")
    print("="*70)
    print("\nInitializing...")
    
    # Setup
    retail_tools = EcommerceTools.get_tools_metadata()
    openai_tools = convert_retail_tools_to_openai(retail_tools, strict=False)
    executors = get_executors()
    client = get_client()
    
    print(f"✅ Loaded {len(retail_tools)} tools")
    print(f"✅ Model: Qwen/Qwen3-Next-80B-A3B-Instruct")
    
    print("\n" + "-"*70)
    print("📋 Available Tools:")
    for i, tool in enumerate(retail_tools, 1):
        print(f"  {i:2d}. {tool['name']:<25} - {tool['description']}")
    
    print("\n" + "="*70)
    print("💡 Instructions:")
    print("  • Enter your message in Russian or English")
    print("  • LLM will automatically select and call appropriate tools")
    print("  • Type 'quit' to exit")
    print("="*70)
    
    messages = []
    
    while True:
        print("\n" + "-"*70)
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Exiting...")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'выход', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Add user message
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        print("\n🤔 LLM thinking...")
        
        try:
            # Get LLM response
            response = client.chat.completions.create(
                model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Check if LLM wants to call tools
            if assistant_message.tool_calls:
                print(f"\n🎯 LLM selected {len(assistant_message.tool_calls)} tool(s):")
                
                # Execute tools
                tool_results = await execute_tool_calls(assistant_message.tool_calls, executors)
                
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Add tool results to messages
                for tr in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tr["tool_call_id"],
                        "content": json.dumps(tr["result"], ensure_ascii=False)
                    })
                
                # Get final response from LLM
                print("\n🤔 LLM processing results...")
                final_response = client.chat.completions.create(
                    model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto"
                )
                
                final_message = final_response.choices[0].message
                
                # Handle if LLM wants to call more tools
                if final_message.tool_calls:
                    print(f"\n🎯 LLM wants to call {len(final_message.tool_calls)} more tool(s):")
                    additional_results = await execute_tool_calls(final_message.tool_calls, executors)
                    
                    messages.append({
                        "role": "assistant",
                        "content": final_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in final_message.tool_calls
                        ]
                    })
                    
                    for tr in additional_results:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tr["tool_call_id"],
                            "content": json.dumps(tr["result"], ensure_ascii=False)
                        })
                    
                    # Get final response after additional tools
                    final_response = client.chat.completions.create(
                        model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                        messages=messages,
                        tools=openai_tools
                    )
                    final_message = final_response.choices[0].message
                
                if final_message.content:
                    print(f"\n💬 Assistant: {final_message.content}")
                    messages.append({
                        "role": "assistant",
                        "content": final_message.content
                    })
                else:
                    print("\n💬 Assistant: [No text response]")
            else:
                # No tools called, just text response
                if assistant_message.content:
                    print(f"\n💬 Assistant: {assistant_message.content}")
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content
                    })
                else:
                    print("\n💬 Assistant: [No response]")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            # Remove last user message on error
            if messages and messages[-1]["role"] == "user":
                messages.pop()


async def main():
    """Entry point"""
    await chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
